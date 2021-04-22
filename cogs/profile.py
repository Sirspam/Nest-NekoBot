import discord
import logging
from discord.ext import commands
from firebase_admin import firestore

dab = firestore.client()


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def profile(self, ctx, user:discord.Member=None):
        return

    @commands.command(case_insensitive=True, aliases=["link","add"])
    async def register(self, ctx):
        logging.info(f"Recieved register {ctx.author.id}")
        col_ref = dab.collection('users').document('collectionlist').get().get('array')
        if str(ctx.author.id) in col_ref:
            return await ctx.reply("You're already in the database!")
        doc_ref = dab.collection("users").document(str(ctx.author.id))
        doc_ref.set({
            "MP": int(0),
        })
        col_ref.append(str(ctx.author.id))
        col_ref.sort()
        dab.collection("users").document("collectionlist").update({"array": col_ref})
        await ctx.reply(f"{ctx.author.name} has sucessfully been added to the database!")
        logging.info(f"{ctx.author.name} has sucessfully been added to the database")


def setup(bot):
    bot.add_cog(Profile(bot))
