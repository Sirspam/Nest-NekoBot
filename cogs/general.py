import logging
from random import choice, randint
from io import BytesIO

from discord import File

from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "jaydz" in message.content.lower():
            return # utter sadness
            if randint(0, 9) == 0:
                await message.reply("jaydeez nuts <:Jaydz1Tf:840275619325673553>")
                logging.info("Posted jaydeez nuts :tf:")
        if message.channel.id == 588471682570649641:
            await message.add_reaction("<:tf:808417609732849664>")

    @commands.command(hidden=True)
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

def setup(bot):
    bot.add_cog(General(bot))
