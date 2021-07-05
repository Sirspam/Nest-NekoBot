import os
import logging
import asyncio

import discord
import aiohttp
from dotenv import load_dotenv

from discord.ext import commands
from utils import jskp


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")


class EmbeddedHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0xfc0000)
            await destination.send(embed=emby)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents, help_command=EmbeddedHelp(), case_insensitive=True, allowed_mentions=discord.AllowedMentions(replied_user=False))


initial_cogs = [
    "jishaku",
    "cogs.error_handler",
    "cogs.general",
    "cogs.status"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession(loop=asyncio.get_event_loop(), headers={"User-Agent": "NestMultiRanking (https://discord.gg/zTCJh8H)"})
    logging.info(f"Bot has successfully launched as {bot.user}")


bot.run(os.getenv("TOKEN"))
