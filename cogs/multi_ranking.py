import discord
import logging
import asyncio
from discord.ext import commands
from firebase_admin import firestore
from utils import ranking_roles

dab = firestore.client()
matches = dict()


class MultiRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def matchstart(self, ctx, member:discord.Member):
        logging.info(f"matchstart invoked by {ctx.author.name} with {member}")
        global matches
        if ctx.author == member:
            await ctx.send("You can't start a match with yourself!")
            return logging.info("author equal to member, match cancelled")
        if dab.collection("users").document(str(ctx.author.id)).get().get("modded") is not dab.collection("users").document(str(member.id)).get().get("modded"):
            await ctx.send("You can't start a match with someone on a different platform to you!")
            return logging.info("modded bools differeated, match cancelled")
        if ctx.author.id in matches.keys():
            await ctx.send("You've already got an open match!")
            return logging.info("author already has an open match, match cancelled")
        col_ref = dab.collection("users").document("collectionlist").get().get('array')
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
                await ctx.send(f"{ctx.author.name} and {member.name}'s match has started!\nBegin playing in multiplayer! Play 3 maps, and who ever wins the most maps gets the most points")
                logging.info(f"Match successfully started. Current matches: {matches}")
            elif str(reaction.emoji) == "❌":
                await ctx.send(f"{member.name} declined. match cancelled")
                logging.info(f"{member.name} declined, match cancelled")

    @commands.command()
    async def matchend(self, ctx):
        logging.info(f"matchend invoked by {ctx.author.name}")
        global matches
        if ctx.author.id not in matches.keys():
            return await ctx.send("You don't have an open match!")
        total = 0
        scores = list()
        for x in matches[ctx.author.id]:
            message = await ctx.send(f"{x.mention} How many maps did you win?")
            await message.add_reaction("0️⃣")
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            def check(reaction, user): # Me copy and pasting the code I stole from the discord.py server B)
                return str(reaction.emoji) in ["0️⃣","1️⃣","2️⃣","3️⃣"] and user == x
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send(f"{x.name} didn't react in time! Please repeat the match end process")
            else:
                if str(reaction.emoji) == "0️⃣":
                    scores.append([0, x])
                if str(reaction.emoji) == "1️⃣":
                    total = total + 1
                    scores.append([1, x])
                if str(reaction.emoji) == "2️⃣":
                    total = total + 2
                    scores.append([2, x])
                if str(reaction.emoji) == "3️⃣":
                    total = total + 3
                    scores.append([3, x])
        if total > 3:
            return await ctx.send("Invalid total! The total wins should be 3! Please repeat the match end process")
        scores.sort(reverse=True)
        await ctx.send(f"{scores[0][1].mention} wins and gains {scores[0][0]}MP! {scores[1][1].mention} loses {scores[0][0]}MP!")
        win_rep = dab.collection("users").document(str(scores[0][1].id)).get() # I hate this block of code
        loss_rep = dab.collection("users").document(str(scores[1][1].id)).get()
        dab.collection("users").document(str(scores[0][1].id)).update({
            "MP": (int(win_rep.get("MP"))+scores[0][0]),
            "wins": (win_rep.get("wins")+1)
        })
        MPLoss = int(loss_rep.get("MP"))-scores[0][0]
        if MPLoss < 0:
            MPLoss = 0
        dab.collection("users").document(str(scores[1][1].id)).update({
            "MP": MPLoss,
            "loses": (loss_rep.get("loses")+1)    
        })
        del matches[ctx.author.id]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def MPset(self, ctx, member:discord.Member, value):
        logging.info(f"MP set invoked by {ctx.author}, setting {member.name} MP to {value}")
        dab.collection("users").document(str(member.id)).update({"MP": value})
        await ranking_roles.assign_rank(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def matches(self, ctx):
        global matches
        await ctx.send(matches)

    """@commands.command() # Leaving this all here in case I need it in the future :)
    async def matchstart(self, ctx, *members:discord.Member):
        logging.info(f"matchstart invoked by {ctx.author.name} with {members}")
        global matches
        if ctx.author.id in matches.keys():
            return await ctx.send("You've already got an open match!")
        players = list()
        y = str()
        col_ref = dab.collection("users").document("collectionlist").get().get('array')
        for x in members:
            if str(x.id) not in col_ref:
                return await ctx.send(f"{x.name} isn't registered!")
            players.append(x.name)
            if x == members[-1]:
                y = y[:-2]+" and "+x.name
                break
            y = y+x.name+", "
        if len(players) < 2:
            return await ctx.send("You can't start a match by yourself!")
        elif len(players) != len(set(players)):
            raise BadArgument
        await ctx.send(f"Match starting between {y}!")
        del y
        for x in members:
                if x == ctx.author:
                    continue
                message = await ctx.send(f"{x.mention} Do you accept the match?")
                await message.add_reaction("✅")
                await message.add_reaction("❌")
                def check(reaction, user): # Me stealing code from the discord.py server B)
                    return str(reaction.emoji) in ["✅","❌"] and user == x
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send(f"{x.name} didn't react in time! match cancelled")
                else:
                    if str(reaction.emoji) == "✅":
                        continue
                    if str(reaction.emoji) == "❌":
                        return await ctx.send(f"{x.name} declined. match cancelled")
        matches.update({ctx.author.id: members})
        await ctx.send(f"{ctx.author.name}'s match has started!\nBegin playing in multiplayer! Play 3 maps, and who ever wins the most maps gets the most points")
        logging.info(f"Match successfully started. Current matches: {matches}")


    @commands.command()
    async def matchend(self, ctx):
        logging.info(f"matchend invoked by {ctx.author.name}")
        global matches
        if ctx.author.id not in matches.keys():
            return await ctx.send("You don't have an open match!")
        total = 0
        scores = dict()
        for x in matches[ctx.author.id]:
            message = await ctx.send(f"{x.mention} Do you accept the match?")
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            def check(reaction, user): # Me copy and pasting the code I stole from the discord.py server B)
                return str(reaction.emoji) in ["1️⃣","2️⃣","3️⃣"] and user == x
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send(f"{x.name} didn't react in time! please repeat the match end process")
            else:
                if str(reaction.emoji) == "1️⃣":
                    total = total + 1
                    scores.update({x: 1})
                if str(reaction.emoji) == "2️⃣":
                    total = total + 1
                    scores.update({x: 2})
                if str(reaction.emoji) == "3️⃣":
                    total = total + 1
                    scores.update({x: 3})
        if total > 3:
            await ctx.send("Invalid total! The total wins should be 3!")"""


def setup(bot):
    bot.add_cog(MultiRanking(bot))
