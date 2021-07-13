import logging
from re import findall
from random import choice
from io import BytesIO
from functools import partial

from discord import File

from discord.utils import get
from discord.ext import commands


async def permitted_roles_check(ctx):
    if ctx.author.guild_permissions.administrator is True:
        return True
    getter = partial(get, ctx.author.roles)
    if any(getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in 232574143818760192):
        return True
    return False

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author.bot is True:
            return
         # Self-promo
        if message.channel.id == 587966826856841226 and not findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",message.content) and not await permitted_roles_check(await self.bot.get_context(message)):
            logging.info(f"Deleting message in #self-promo by {message.author.name}:\n{message.content}")
            await message.delete()
            async with self.bot.session.get("https://cdn.discordapp.com/attachments/641750796781879307/779705559800610826/bug_off_wanker.png") as resp:
                await message.author.send(file=File(BytesIO(await resp.read()), "bog_off_wanker.png"))
        # Announcements
        if message.channel.id == 588471682570649641:
            logging.info("Reacted to announcement message :tf:")
            await message.add_reaction("<:tf:808417609732849664>")

    @commands.command()
    async def neko(self, ctx):
        # Hmm yes, hard corded database B)
        async with self.bot.session.get(choice([
        "https://cdn.discordapp.com/emojis/786584088403509338.png",
        "https://cdn.discordapp.com/attachments/587749898729029648/839806693621760000/Untitled138_20210505215431.png",
        "https://cdn.discordapp.com/attachments/587749898729029648/839807192601198602/Untitled138_20210505210112.png",
        "https://media.discordapp.net/attachments/734485591248338954/736429296830119946/nug.png",
        "https://media.discordapp.net/attachments/734485591248338954/736687338822041670/unknown.png",
        "https://media.discordapp.net/attachments/734485591248338954/734932336789028935/nugdog.png",
        "https://media.discordapp.net/attachments/734485591248338954/734810660386635816/doggo.jpeg",
        "https://media.discordapp.net/attachments/734485591248338954/734732953263013948/unknown.png?",
        "https://media.discordapp.net/attachments/734485591248338954/734539889269538877/unknown.png",
        "https://media.discordapp.net/attachments/734485591248338954/734506492140585010/chickn.png",
        "https://media.discordapp.net/attachments/734485591248338954/734501737905389658/nug_dog.png",
        "https://media.discordapp.net/attachments/734485591248338954/734492811935744080/unknown.png",
        "https://media.discordapp.net/attachments/734485591248338954/734899965821845685/bigjaydz.jpg",
        "https://media.discordapp.net/attachments/587749898729029648/840017181063905300/Untitled139_20210506071635.png",
        "https://media.discordapp.net/attachments/734485591248338954/736930199593287701/Becoom_nugdog.png",
        "https://media.discordapp.net/attachments/734485591248338954/735002105248612432/unknown-55.png",
        "https://cdn.discordapp.com/attachments/644475427770859530/841766393406029834/Untitled145.png",
        "https://cdn.discordapp.com/attachments/644475427770859530/841766777080119356/Untitled144_20210509233227.png"
        ])) as resp:
                await ctx.reply(file=File(BytesIO(await resp.read()), "cute_kawaii_neko.png"))

    @commands.command()
    async def wanker(self, ctx):
        async with self.bot.session.get("https://cdn.discordapp.com/attachments/641750796781879307/779705559800610826/bug_off_wanker.png") as resp:
            await ctx.reply(file=File(BytesIO(await resp.read()), "bog_off_wanker.png"))


def setup(bot):
    bot.add_cog(General(bot))
