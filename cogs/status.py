import logging

from discord import Game, Activity, ActivityType
from random import choice, getrandbits

from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @tasks.loop(minutes=30)
    async def status(self):
        await self.bot.wait_until_ready()
        if getrandbits(1) == 1:
            value = choice([ # Playing
                "Beat Saber",
                "Shiny Happy Days on loop",
                "with Sirspam's final braincell",
                "with nekos",
                "with booba 😳",
                "😎"
            ])
            await self.bot.change_presence(activity=Game(name=value))
            logging.info(f"Status set to: {value}")
        else:
            value = choice([ # Watching
                f"{self.bot.get_guild(587749898045095960).member_count} people"
                "Jaydz live on twitch",
                "You.",
                "Dan make a fool of himself",
                "Soberra throwing a fit",
                "Dan p :tf:",
                "Dicone be cool",
                "Gavin on the porch",
                "Carl's Jr get banned again",
                "Bitz desperately rolling for waifus",
                "Goose ad sddufba",
                "Skip skip skippety skip skip skip",
                "Bitz suggest awful statuses",
                "Mar fangirl over Jaydz",
                "Pigeon waste her primogems"
            ])
            await self.bot.change_presence(activity=Activity(name=value, type=ActivityType.watching))
            logging.info(f"Status set to: {value}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()


def setup(bot):
    bot.add_cog(Status(bot))
