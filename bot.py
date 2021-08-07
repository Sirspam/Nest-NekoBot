import logging
from os import getcwd, getenv
from asyncio import get_event_loop

from discord import Intents, AllowedMentions
from aiohttp import ClientSession
from dotenv import load_dotenv

from discord.ext.commands import Bot
from utils import jskp


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)

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
bot.default_prefix = getenv("DEFAULT_PREFIX")
bot.github_repo = getenv("GITHUB_REPO_URL")
try:
    bot.logging_channel_id = int(getenv("LOGGING_CHANNEL_ID"))
except TypeError:
    bot.logging_channel_id = None

initial_cogs = [
    "jishaku",
    "cogs.beatsaver",
    "cogs.error_handler",
    "cogs.fun",
    "cogs.help",
    "cogs.information",
    "cogs.listeners",
    "cogs.moderation",
    "cogs.status"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


async def startup():
    await bot.wait_until_ready()
    bot.session = ClientSession(loop=get_event_loop(), headers={"User-Agent": getenv("USER_AGENT")})
    bot.owner_id = (await bot.application_info()).owner.id

bot.loop.create_task(startup())


@bot.before_invoke
async def before_invoke(ctx):
    logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name} ({ctx.message.content})" )
@bot.after_invoke
async def after_invoke(ctx):
    logging.info(f"Concluded {ctx.command}")


bot.run(getenv("TOKEN"))
