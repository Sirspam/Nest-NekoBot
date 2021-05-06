import discord
import logging
from random import getrandbits
from random import choice
from discord.ext import commands
from io import BytesIO


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Flips a coin",aliases=["flip"])
    async def coin(self, ctx):
        logging.info("Coin invoked")
        if getrandbits(1) == 1:
            await ctx.reply("Heads")
        else:
            await ctx.reply("Tails")
        logging.info("Coin ended")

    @commands.command(help="Generates a random bsr key (WIP)")
    async def bsr(self, ctx):
        logging.info("bsr invoked")
        await ctx.send("e970")
        logging.info("bsr ran")

    @commands.command(hidden=True)
    async def neko(self, ctx):
        # Hmm yes, hard corded database B)
        async with self.bot.session.get(choice(["https://cdn.discordapp.com/emojis/786584088403509338.png",
        "https://cdn.discordapp.com/attachments/587749898729029648/839806693621760000/Untitled138_20210505215431.png",
        "https://cdn.discordapp.com/attachments/587749898729029648/839807192601198602/Untitled138_20210505210112.png"])) as resp:
                await ctx.reply(file=discord.File(BytesIO(await resp.read()), "cute_kawaii_neko.png"))

def setup(bot):
    bot.add_cog(General(bot))
