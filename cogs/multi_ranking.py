import discord
import logging
import asyncio
from discord.ext import commands
from firebase_admin import firestore
from utils import ranking_roles


dab = firestore.client()
matches = dict()
active_participants = list()


class MultiRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Starts a match with one other user")
    async def matchstart(self, ctx, member:discord.Member):
        logging.info(f"matchstart invoked by {ctx.author.name} with {member}")
        global matches
        if ctx.author == member:
            await ctx.send("You can't start a match with yourself!")
            return logging.info("author equal to member, match cancelled")
        if dab.collection("users").document(str(ctx.author.id)).get().get("modded") is not dab.collection("users").document(str(member.id)).get().get("modded"):
            await ctx.send("You can't start a match with someone on a different platform to you!")
            return logging.info("modded bools differeated, match cancelled")
        if ctx.author.id in active_participants:
            await ctx.send("You've already got an open match!")
            return logging.info("author already has an open match, match cancelled")
        if member.id in active_participants:
            await ctx.send("You're already in an open match!")
            return logging.info("member already in an open match, match cancalled")
        col_ref = dab.collection("users").document("collectionlist").get().get('users')
        if str(member.id) not in col_ref:
            return await ctx.send(f"{member.name} isn't registered!")
        if str(ctx.author.id) not in col_ref:
            return await ctx.send(f"{ctx.author.name} isn't registered!")
        await ctx.send(f"Match starting between {ctx.author.name} and {member.name}!")
        message = await ctx.send(f"{member.mention} Do you accept the match?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def check(reaction, user): # Me stealing code from the discord.py server B)
            return str(reaction.emoji) in ["✅","❌"] and user == member
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send(f"{member.name} didn't react in time! match cancelled")
        else:
            if str(reaction.emoji) == "✅":
                matches.update({ctx.author.id: (ctx.author,member)})
                active_participants.append(ctx.author.id)
                active_participants.append(member.id)
                await ctx.send(f"{ctx.author.name} and {member.name}'s match has started!\nBegin playing in multiplayer! Play 3 maps, and who ever wins the most maps gets the most points")
                logging.info(f"Match successfully started. Current matches: {matches}")
            elif str(reaction.emoji) == "❌":
                await ctx.send(f"{member.name} declined. match cancelled")
                logging.info(f"{member.name} declined, match cancelled")

    @commands.command(help="Ends the author's current match")
    async def matchend(self, ctx):
        logging.info(f"matchend invoked by {ctx.author.name}")
        global matches
        if ctx.author.id not in matches.keys():
            return await ctx.send("You don't have an open match!")
        total = 0
        scores = list()
        message = await ctx.send(f"{ctx.author.mention} How many maps did you win?")
        await message.add_reaction("0️⃣")
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        def val_check(reaction, user): # Me copy and pasting the code I stole from the discord.py server B)
            return str(reaction.emoji) in ["0️⃣","1️⃣","2️⃣","3️⃣"] and user == ctx.author
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=val_check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author} didn't react in time! Please repeat the match end process")
        else:
            if str(reaction.emoji) == "0️⃣":
                scores.append([0, ctx.author])
            if str(reaction.emoji) == "1️⃣":
                scores.append([1, ctx.author])
            if str(reaction.emoji) == "2️⃣":
                scores.append([2, ctx.author])
            if str(reaction.emoji) == "3️⃣":
                scores.append([3, ctx.author])
        scores.append([(3-scores[0][0]),matches[ctx.author.id][1]])
        scores.sort(reverse=True)
        message = await ctx.send(f"The score is **{scores[0][0]} - {scores[1][0]} to {scores[0][1].name}**\n{matches[ctx.author.id][1].mention} do you agree to this score?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def validation_check(reaction, user):
            return str(reaction.emoji) in ["✅","❌"] and user == matches[ctx.author.id][1]
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=validation_check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send("You didn't respond in time!")
        if str(reaction.emoji) == "✅":
            await ctx.send(f"{scores[0][1].mention} wins and gains {scores[0][0]}MP! {scores[1][1].mention} loses {scores[0][0]}MP!")
            win_rep = dab.collection("users").document(str(scores[0][1].id)).get() # I hate this block of code
            win_rank = await ranking_roles.determine_rank(ctx, int(win_rep.get("MP"))+scores[0][0])
            loss_rep = dab.collection("users").document(str(scores[1][1].id)).get()
            dab.collection("users").document(str(scores[0][1].id)).update({
                "MP": (int(win_rep.get("MP"))+scores[0][0]),
                "wins": (win_rep.get("wins")+1),
                "rank": win_rank
            })
            MPLoss = int(loss_rep.get("MP"))-scores[0][0]
            if MPLoss < 0:
                MPLoss = 0
            loss_rank = await ranking_roles.determine_rank(ctx, MPLoss)
            dab.collection("users").document(str(scores[1][1].id)).update({
                "MP": MPLoss,
                "loses": (loss_rep.get("loses")+1),
                "rank": loss_rank
            })
            count = 0
            for x in self.bot.leaderboard: # For the love of god please rewrite this at some point
                if x[0]==(str(scores[0][1].id)):
                    self.bot.leaderboard[count] = (x[0],int(win_rep.get("MP"))+scores[0][0],await ranking_roles.return_emote(win_rank))
                if x[0]==(str(scores[1][1].id)):
                    self.bot.leaderboard[count] = (x[0],MPLoss,await ranking_roles.return_emote(loss_rank))
                count = count + 1
            self.bot.leaderboard.sort(key=lambda a: a[1], reverse=True)
            del matches[ctx.author.id]
        if str(reaction.emoji) == "❌":
            return await ctx.send(f"{matches[ctx.author.id][1].name} has declined this score. please redo the matchend process or contact a moderator")

    @commands.command()
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def admin_matchend(self, ctx, match_owner:discord.Member):
        logging.info(f"admin_matchend invoked by {ctx.author.name}. {match_owner.name} passed as match_owner")
        global matches
        if match_owner.id not in matches.keys():
            return await ctx.send(f"{match_owner.name} doesn't have an open match")
        total = 0
        scores = list()
        message = await ctx.send(f"How many maps did __{match_owner.name}__ you win?")
        await message.add_reaction("0️⃣")
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        def val_check(reaction, user): # Me copy and pasting the code I stole from the discord.py server B)
            return str(reaction.emoji) in ["0️⃣","1️⃣","2️⃣","3️⃣"] and user == ctx.author
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=val_check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author} didn't react in time! Please repeat the match end process")
        else:
            if str(reaction.emoji) == "0️⃣":
                scores.append([0, match_owner])
            if str(reaction.emoji) == "1️⃣":
                scores.append([1, match_owner])
            if str(reaction.emoji) == "2️⃣":
                scores.append([2, match_owner])
            if str(reaction.emoji) == "3️⃣":
                scores.append([3, match_owner])
        scores.append([(3-scores[0][0]),matches[match_owner.id][1]])
        scores.sort(reverse=True)
        message = await ctx.send(f"The score is **{scores[0][0]} - {scores[1][0]} to {scores[0][1].name}**\nIs this score correct?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def validation_check(reaction, user):
            return str(reaction.emoji) in ["✅","❌"] and user == ctx.author
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=validation_check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send("You didn't respond in time!")
        if str(reaction.emoji) == "✅":
            await ctx.send(f"{scores[0][1].mention} wins and gains {scores[0][0]}MP! {scores[1][1].mention} loses {scores[0][0]}MP!")
            win_rep = dab.collection("users").document(str(scores[0][1].id)).get() # I hate this block of code
            win_rank = await ranking_roles.determine_rank(ctx, int(win_rep.get("MP"))+scores[0][0])
            loss_rep = dab.collection("users").document(str(scores[1][1].id)).get()
            dab.collection("users").document(str(scores[0][1].id)).update({
                "MP": (int(win_rep.get("MP"))+scores[0][0]),
                "wins": (win_rep.get("wins")+1),
                "rank": win_rank
            })
            MPLoss = int(loss_rep.get("MP"))-scores[0][0]
            if MPLoss < 0:
                MPLoss = 0
            loss_rank = await ranking_roles.determine_rank(ctx, MPLoss)
            dab.collection("users").document(str(scores[1][1].id)).update({
                "MP": MPLoss,
                "loses": (loss_rep.get("loses")+1),
                "rank": loss_rank
            })
            count = 0
            for x in self.bot.leaderboard: # For the love of god please rewrite this at some point
                if x[0]==(str(scores[0][1].id)):
                    self.bot.leaderboard[count] = (x[0],int(win_rep.get("MP"))+scores[0][0],await ranking_roles.return_emote(win_rank))
                if x[0]==(str(scores[1][1].id)):
                    self.bot.leaderboard[count] = (x[0],MPLoss,await ranking_roles.return_emote(loss_rank))
                count = count + 1
            self.bot.leaderboard.sort(key=lambda a: a[1], reverse=True)
            del matches[match_owner.id]
        if str(reaction.emoji) == "❌":
            return await ctx.send(f"{matches[match_owner.id][1].name} has declined this score. please redo the matchend process or contact a moderator")

    
    @commands.command(help="Posts the requirements for each rank",aliases=["ranks"])
    async def rankings(self, ctx):
        logging.info("rankings invoked")
        await ctx.send(embed=discord.Embed(
            title="MP Ranks",
            description=await ranking_roles.rank_list(),
            colour=0xfc0000))
        logging.info("rankings ended")
    
    @commands.command(help="Sets a user's MP value to the specified value")
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def MPset(self, ctx, member:discord.Member, value):
        logging.info(f"MP set invoked by {ctx.author}, setting {member.name} MP to {value}")
        ctx.author = member
        dab.collection("users").document(str(member.id)).update({"MP": value})
        count = 0
        for x in self.bot.leaderboard: # For the love of god please rewrite this at some point
            if x[0]==(str(member.id)):
                self.bot.leaderboard[count] = (x[0],int(value),await ranking_roles.return_emote(await ranking_roles.determine_rank(ctx, int(value))))
            count = count + 1
        self.bot.leaderboard.sort(key=lambda a: a[1], reverse=True)
        await ranking_roles.assign_rank(ctx, int(value))
        await ctx.message.add_reaction("✅")

    @commands.command(help="Posts the current matches (debug)")
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def matches(self, ctx):
        global matches
        await ctx.send(matches)


def setup(bot):
    bot.add_cog(MultiRanking(bot))
