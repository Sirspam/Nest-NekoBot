import logging
from random import choice
from os import listdir

from discord import File

from discord.utils import get
from discord.ext import commands


async def permitted_roles_check(ctx):
    if ctx.author.guild_permissions.administrator or get(ctx.author.roles, id=587963873186021376):
        return True
    return False

class Fun(commands.Cog):
    "Fun Commands for doing funnies"
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # Announcements
        if message.channel.id == 588471682570649641:
            logging.info("Reacted to announcement message :tf:")
            await message.add_reaction("<:tf:808417609732849664>")
        if message.content == "<@!835514928357441556> my beloved":
            await message.reply(file=File(self.bot.cwd+"//assets//nekobot_my_beloved.gif"))

    @commands.command(aliases=["nya"], help="Posts a kawaii ~~nug dog~~ neko")
    async def neko(self, ctx):
        attachment_path = self.bot.cwd+"//assets//nekos//birthday"
        attachment_name = choice(listdir(attachment_path))
        attachment_path += "//" + attachment_name
        await ctx.reply(file=File(attachment_path, f"kawaii_neko_{attachment_name}"))

    @commands.command(aliases=["bog_off_wanker"], help="bog off wanker")
    async def wanker(self, ctx):
        await ctx.reply(file=File(self.bot.cwd+"/assets/bog_off_wanker.png"))


def setup(bot):
    bot.add_cog(Fun(bot))
