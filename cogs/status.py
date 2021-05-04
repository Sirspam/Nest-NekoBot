import discord
import logging
from discord.ext import commands
from discord.ext import tasks
from random import choice
from random import getrandbits


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @tasks.loop(hours=1)
    async def status(self):
        await self.bot.wait_until_ready()
        if getrandbits(1) == 1:
            value = choice([
                "Beat Saber",
                "Shiny Happy Days on loop",
                "with Sirspam's final braincell",
                f"with {self.bot.guild_meber_count}"
            ])
            await self.bot.change_presence(activity=discord.Game(name=value))
            logging.info(f"Status set to: {value}")
        else:
            value = choice([
                "Jaydz live on twitch",
                "Bitz live on twitch :PeepoStare:",
                "Sirspam live on twitch",
                "Soberra live on twitch",
                "Sckuffles live on twitch",
                "for .matchstart",
                "You",
                "Dan make a fool of himself",
                "Soberra throwing a fit",
                "Dan p :tf:",
                "Dicone be cool",
                "Gavin on the porch",
                "Carl's Jr get banned again",
                "Bitz desperately rolling for waifus",
                "Goose ad sddufba",
                "Monke on youtube",
                "Skip skip skippety skip skip skip",
                "Bitz suggest awful statuses",
                "Mar fangirl over Jaydz"
            ])
            await self.bot.change_presence(activity=discord.Activity(name=value, type=discord.ActivityType.watching))
            logging.info(f"Status set to: {value}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(Status(bot))
