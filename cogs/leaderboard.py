import discord
import logging
from discord.ext import commands
#from discord.ext import menus
from discord.ext.commands.errors import BadArgument
from firebase_admin import firestore
from utils import ranking_roles


dab = firestore.client()
"""
class LeaderboardMenu(menus.Menu):
    #def __init__(self):
        #return
    
    async def send_initial_message(self, ctx, type, channel):
        logging.info("leaderboard invoked")
        segregated_leaderboard = list()
        if type.lower()=="modded":
            logging.info("modded type")
            type_collectionlist = dab.collection("users").document("collectionlist").get().get("modded")
            for x in self.bot.leaderboard:
                if x[0] in type_collectionlist:
                    segregated_leaderboard.append(x)
            title = "(Modded)"
        elif type.lower()=="quest":
            logging.info("quest type")
            type_collectionlist = dab.collection("users").document("collectionlist").get().get("quest")
            for x in self.bot.leaderboard:
                if x[0] in type_collectionlist:
                    segregated_leaderboard.append(x)
            title = "(Quest)"
        elif type.lower()=="all":
            logging.info("all type")
            segregated_leaderboard=self.bot.leaderboard
            title = "(All)"
        else:
            raise BadArgument
        count = 1
        page_count = 0 
        pages = list()
        message = str()
        for x in segregated_leaderboard:
            if page_count == 15:
                pages.append(message)
                message = str()
                page_count = 0
                #print(pages)
            member = ctx.guild.get_member(int(x[0]))
            if member is None:
                continue
            message = message+f"{await ranking_roles.return_emote(x[2])} #{count} - ``{member.name}`` - MP: {x[1]}\n"
            count = count+1
            page_count = page_count+1
        embed = discord.Embed(
            title = f"Nest Multi Ranking Leaderboard {title}",
            description = pages[0],
            colour = 0xfc0000,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=(ctx.guild.get_member(int(segregated_leaderboard[0][0]))).avatar_url)
        return await ctx.send(embed=embed)


    @menus.button("\N{BLACK LEFT-POINTING TRIANGLE}")
    async def on_back(self, payload):
        embed = discord.Embed(
            title = f"Nest Multi Ranking Leaderboard {title}",
            description = pages[0],
            colour = 0xfc0000,
            timestamp=self.ctx.message.created_at
        )
        await self.message.edit(content="cunt")

    @menus.button("\N{BLACK RIGHT-POINTING TRIANGLE}")
    async def on_forward(self, payload):
        await self.message.edit(content="nonce")

    @menus.button("\N{BLACK SQUARE FOR STOP}")
    async def on_stop(self, payload):
        self.stop()
"""

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #@commands.command()
    #async def cringe(self, ctx):
    #    type = "All"
    #    await LeaderboardMenu().start(ctx, wait=True)
    
    @commands.command(help="Posts a leaderboard of the individiuals with the most MP\nValid arguments are ``all``, ``modded`` and ``quest``")
    async def leaderboard(self, ctx, type="all"):
        logging.info("leaderboard invoked")
        segregated_leaderboard = list()
        if type.lower()=="modded":
            logging.info("modded type")
            type_collectionlist = dab.collection("users").document("collectionlist").get().get("modded")
            for x in self.bot.leaderboard:
                if x[0] in type_collectionlist:
                    segregated_leaderboard.append(x)
            title = "(Modded)"
        elif type.lower()=="quest":
            logging.info("quest type")
            type_collectionlist = dab.collection("users").document("collectionlist").get().get("quest")
            for x in self.bot.leaderboard:
                if x[0] in type_collectionlist:
                    segregated_leaderboard.append(x)
            title = "(Quest)"
        elif type.lower()=="all":
            logging.info("all type")
            segregated_leaderboard=self.bot.leaderboard
            title = "(All)"
        else:
            raise BadArgument
        count = 1
        page_count = 0 
        pages = list()
        message = str()
        for x in segregated_leaderboard:
            if page_count == 15:
                pages.append(message)
                message = str()
                page_count = 0
                #print(pages)
            member = ctx.guild.get_member(int(x[0]))
            if member is None:
                continue
            message = message+f"{x[2]} #{count} - ``{member.name}`` - MP: {x[1]}\n"
            count = count+1
            page_count = page_count+1
        if pages == []:
            pages.append(message)
        embed = discord.Embed(
            title = f"Nest Multi Ranking Leaderboard {title}",
            description = pages[0],
            colour = 0xfc0000,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=(ctx.guild.get_member(int(segregated_leaderboard[0][0]))).avatar_url)
        await ctx.send(embed=embed)

    @commands.command(hidden=True, help="Generates the leaderboard from firebase (debug)")
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def generate_leaderboard(self, ctx):
        logging.info(f"generate_leaderboard invoked by {ctx.author.name}")
        async with ctx.channel.typing():
            await populate_leaderboard(self)
        logging.info(self.bot.leaderboard)
        await ctx.message.add_reaction("✅")
    
    @commands.Cog.listener()
    async def on_ready(self):
        await populate_leaderboard(self)


def setup(bot):
    bot.add_cog(Leaderboard(bot))


async def populate_leaderboard(self):
    logging.info("populate_leaderboard invoked")
    self.bot.leaderboard=list()
    for x in dab.collection("users").document("collectionlist").get().get("users"):
        ref = dab.collection("users").document(str(x)).get()
        mp = int(ref.get("MP")) # sort didn't like it if I wasn't defining mp outside of the append function, for some reason
        rank_emote = await ranking_roles.return_emote(str(ref.get("rank")))
        self.bot.leaderboard.append((x,mp,rank_emote))
    self.bot.leaderboard.sort(key=lambda a: a[1], reverse=True)
    logging.info("populate_leaderboard concluded")
    