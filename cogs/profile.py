import discord
import logging
import asyncio
from discord.ext import commands
from firebase_admin import firestore
from os import getcwd
from random import randint


dab = firestore.client()
badge_directory = getcwd()+"//images//badges"

badge_colours = {    
    "Bronze":"cd7f32",
    "Silver":"949494",
    "Gold":"e8bd12",
    "Platinum":"c0c0c0",
    "Diamond":"00ddff",
    "Master":"9600ff",
    }


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["p"], help="Posts the profile for the author or mentioned user")
    async def profile(self, ctx, user:discord.Member=None):
        if user is not None:
            ctx.author = user
        if str(ctx.author.id) not in dab.collection("users").document("collectionlist").get().get("users"):
            return await ctx.send("You haven't registered for a profile!")
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        rank = ref.get("rank")
        wins = ref.get("wins")
        loses = ref.get("loses")
        if rank == "Master":
            if randint(0,10) == 0:
                badge_path = badge_directory+"//Crime.png"
            else:
                badge_path = badge_directory+"//Master.png"
        else:
            badge_path = badge_directory+"//"+rank+".png"
        embed = discord.Embed(
            description="",
            colour=await commands.ColourConverter().convert(ctx, "0x"+badge_colours[rank]),
            timestamp=ctx.message.created_at
            )
        embed.set_author(name=ctx.author.name,icon_url=str(ctx.author.avatar_url))
        embed.add_field(name="MultiPoints", value=ref.get("MP"), inline=False)
        embed.add_field(name="Rank", value=rank, inline=False)
        embed.add_field(name="Wins", value=wins, inline=True)
        embed.add_field(name="Loses", value=loses, inline=True)
        try:
            embed.add_field(name="WL Ratio", value=round(wins/loses,2), inline=True)
        except ZeroDivisionError:
            embed.add_field(name="WL Ratio", value=0, inline=True)
        file = discord.File(badge_path, filename="image.png")
        embed.set_thumbnail(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(aliases=["link","add"], help="Registers the author to the database")
    async def register(self, ctx):
        logging.info(f"Recieved register {ctx.author.id}")
        col_ref = dab.collection("users").document("collectionlist").get().get("users")
        if str(ctx.author.id) in col_ref:
            await ctx.reply("You're already in the database!")
            return logging.info("User already in database")
        message = await ctx.reply("Do you play __vanilla quest__ with no mods?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        def check(reaction, user):
            return str(reaction.emoji) in ["✅","❌"] and user == ctx.author
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send("You didn't respond in time!")
        if str(reaction.emoji) == "❌":
            modded = True
            message = await ctx.send("Do you want to be pinged whenever another modded player wants to play?\nKeep in mind you may be pinged frequently!")
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't respond in time!")
            if str(reaction.emoji) == "✅":
                await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, "792949628940451851"))
        elif str(reaction.emoji) == "✅":
            modded = False
            message = await ctx.send("Do you want to be pinged whenever another non modded player wants to play?\nKeep in mind you may be pinged frequently!")
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send("You didn't respond in time!")
            if str(reaction.emoji) == "✅":
                await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, "792949630500470804"))
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.set({
            "MP": int(0),
            "rank": "Bronze",
            "wins": int(0),
            "loses": int(0),
            "modded": modded
        })
        col_ref.append(str(ctx.author.id))
        col_ref.sort()
        dab.collection("users").document("collectionlist").update({"users": col_ref})
        if modded is True:
            print("modded true")
            list_ref = dab.collection("users").document("collectionlist").get().get("modded")
            list_ref.append(str(ctx.author.id))
            list_ref.sort()
            dab.collection("users").document("collectionlist").update({"modded": list_ref})
        elif modded is False:
            print("modded false")
            list_ref = dab.collection("users").document("collectionlist").get().get("quest")
            list_ref.append(str(ctx.author.id))
            list_ref.sort()
            print(list_ref)
            dab.collection("users").document("collectionlist").update({"quest": list_ref})
        #await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, "835882077298622465"))
        await ctx.send(f"{ctx.author.name} has successfully registered!")
        logging.info(f"{ctx.author.name} has successfully been added to the database")

    @commands.command(aliases=["register'nt"], help="Removes the author from the database")
    async def remove(self, ctx):
        logging.info(f"remove raised by {ctx.author.name}")
        modded = dab.collection("users").document(str(ctx.author.id)).get().get("modded")
        col_ref = dab.collection("users").document("collectionlist").get().get("users")
        col_ref.remove(str(ctx.author.id))
        dab.collection("users").document("collectionlist").update({"users": col_ref})
        dab.collection("users").document(str(ctx.author.id)).delete()
        print(modded)
        if modded is True:
            col_ref = dab.collection("users").document("collectionlist").get().get("modded")
            col_ref.remove(str(ctx.author.id))
            dab.collection("users").document("collectionlist").update({"modded": col_ref})
        elif modded is False:
            col_ref = dab.collection("users").document("collectionlist").get().get("quest")
            col_ref.remove(str(ctx.author.id))
            dab.collection("users").document("collectionlist").update({"quest": col_ref})
        await ctx.send("Successfully removed you from the database!")
        logging.info(f"{ctx.author.name} successfully removed from the database")


def setup(bot):
    bot.add_cog(Profile(bot))
