import discord
import logging
import asyncio
from discord.ext import commands
from firebase_admin import firestore

dab = firestore.client()


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["p"])
    async def profile(self, ctx, user:discord.Member=None):
        if user is not None:
            ctx.author = user
        if str(ctx.author.id) not in dab.collection("users").document("collectionlist").get().get("array"):
            return await ctx.send("You haven't registered for a profile!")
        ref = dab.collection("users").document(str(ctx.author.id)).get()
        embed = discord.Embed(
            title=ctx.author.name,
            colour=discord.Colour.random())
        embed.add_field(name="MultiPoints", value=ref.get("MP"), inline=False)
        embed.add_field(name="Rank", value=ref.get("rank"), inline=False)
        wins = ref.get("wins")
        loses = ref.get("loses")
        embed.add_field(name="Wins", value=wins, inline=True)
        embed.add_field(name="Loses", value=loses, inline=True)
        try:
            embed.add_field(name="WL Ratio", value=round(wins/loses,2), inline=True)
        except ZeroDivisionError:
            embed.add_field(name="WL Ratio", value=0, inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["link","add"])
    async def register(self, ctx):
        logging.info(f"Recieved register {ctx.author.id}")
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            await ctx.reply("You're already in the database!")
            return logging.info("User already in database")
        message = await ctx.reply("Do you play on __non modded__ quest?")
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
                await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, "835212978508529675"))
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
                await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, "835213010980438016"))
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
        dab.collection("users").document("collectionlist").update({"array": col_ref})
        await ctx.reply(f"{ctx.author.name} has sucessfully been added to the database!")
        logging.info(f"{ctx.author.name} has sucessfully been added to the database")

    @commands.command(aliases=["register'nt"])
    async def remove(self, ctx):
        logging.info(f"remove raised by {ctx.author.name}")
        col_ref = dab.collection("users").document("collectionlist").get().get("array")
        col_ref.remove(str(ctx.author.id))
        dab.collection("users").document("collectionlist").update({"array": col_ref})
        dab.collection("users").document(str(ctx.author.id)).delete()
        await ctx.send("Successfully removed you from the database!")
        logging.info(f"{ctx.author.name} successfully removed from the database")


def setup(bot):
    bot.add_cog(Profile(bot))
