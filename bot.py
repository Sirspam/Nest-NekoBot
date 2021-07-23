import logging
from os import getcwd, getenv
from asyncio import get_event_loop

from discord import Intents, AllowedMentions
from aiohttp import ClientSession
from dotenv import load_dotenv

from discord.ext.commands import Bot
from utils import jskp


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

cwd = getcwd()
load_dotenv(f"{cwd}/.env")


intents = Intents.default()
intents.members = True
bot = Bot(
    command_prefix=getenv("PREFIX"), 
    intents=intents, 
    case_insensitive=True, 
    allowed_mentions=AllowedMentions(
        everyone=False,
        roles=False,
        replied_user=False
    )
)
bot.cwd = cwd

initial_cogs = [
    "jishaku",
    "cogs.beatsaver",
    "cogs.error_handler",
    "cogs.general",
    "cogs.moderation",
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
    bot.logger_channel = bot.get_channel(864913000284422144)
    bot.session = ClientSession(loop=get_event_loop(), headers={"User-Agent": getenv("USER_AGENT")})
    logging.info(f"Bot has successfully launched as {bot.user}")

@bot.before_invoke
async def before_invoke(ctx):
    logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}")

@bot.after_invoke
async def after_invoke(ctx):
    logging.info(f"Concluded {ctx.command}")


bot.run(getenv("TOKEN"))
