import discord
import logging
from discord.ext import commands
from discord.ext import menus
from discord.ext.commands.errors import BadArgument
from firebase_admin import firestore
from utils import ranking_roles


dab = firestore.client()

class LeaderboardMenu(menus.ListPageSource):
    def __init__(self, data, embed):
        super().__init__(data, per_page=15)
        self.embed = embed

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        self.embed.clear_fields()
        self.embed.add_field(
            name="\u200b",
            value='\n'.join(f"#{i+1} <@{v[0]}> MP: **{v[1]}** {v[2]}" for i, v in enumerate(entries, start=offset)),
            inline=True
        )
        self.embed.set_footer(text=f"Page {(menu.current_page+1)}/{self.get_max_pages()}")
        return self.embed


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(help="Posts a leaderboard of the individiuals with the most MP\nValid arguments are ``all``, ``modded`` and ``quest``",aliases=["lb"])
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
        embed = discord.Embed(
            title = f"Nest Multi Ranking Leaderboard {title}",
            colour = 0xfc0000,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=(ctx.guild.get_member(int(segregated_leaderboard[0][0]))).avatar_url)
        pages = menus.MenuPages(source=LeaderboardMenu(segregated_leaderboard, embed), timeout=30.0, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(hidden=True, help="Generates the leaderboard from firebase (debug)")
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def generate_leaderboard(self, ctx):
        logging.info(f"generate_leaderboard invoked by {ctx.author.name}")
        async with ctx.channel.typing():
            await populate_leaderboard(self)
            await ctx.message.add_reaction("✅")
        logging.info(self.bot.leaderboard)

    @commands.command(hidden=True, help="Generates the leaderboard from firebase (debug)")
    @commands.has_any_role(*[769117646280982538,587963873186021376])
    async def clean_database(self, ctx):
        logging.info(f"clean_database invoked by {ctx.author.name}")
        async with ctx.channel.typing():
            await clean_database(self, ctx)
            await ctx.message.add_reaction("✅")
        logging.info("clean_database concluded")

    @commands.Cog.listener()
    async def on_member_remove(member):
        await clean_database
    
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
    
async def clean_database(self, ctx):
    logging.info("clean_database invoked")
    ref = dab.collection("users").document("collectionlist").get().get("users")
    modded_ref = dab.collection("users").document("collectionlist").get().get("modded")
    quest_ref = dab.collection("users").document("collectionlist").get().get("quest")
    for x in ref:
        print(x)
        if ctx.guild.get_member(int(x)) is None:
            ref.remove(x)
            dab.collection("users").document(str(x)).delete()
            if str(x) in modded_ref:
                modded_ref.remove(x)
            elif str(x) in quest_ref:
                quest_ref.remove(x)
    dab.collection("users").document("collectionlist").update({"users": ref})
    dab.collection("users").document("collectionlist").update({"modded": modded_ref})
    dab.collection("users").document("collectionlist").update({"quest": quest_ref})
    logging.info("clean_database concluded")
    await populate_leaderboard(self)