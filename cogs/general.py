import discord
import logging
from random import getrandbits
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Flips a coin")
    async def coin(self, ctx):
        logging.info("Coin ran")
        if getrandbits(1) == 1:
            await ctx.reply("Heads")
        else:
            await ctx.reply("Tails")
        logging.info("Coin ended")


def setup(bot):
    bot.add_cog(General(bot))