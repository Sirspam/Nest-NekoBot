import discord
import os
import logging
import firebase_admin
from discord.ext import commands
from firebase_admin import credentials
from dotenv import load_dotenv
from utils import jskp


cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "nest-multi-ranking",
  "private_key_id": "f169c1372959aa363852049b3774c0359e9cc69a",
  "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": "firebase-adminsdk-yt46m@nest-multi-ranking.iam.gserviceaccount.com",
  "client_id": "116002653078212367893",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yt46m%40nest-multi-ranking.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)



intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents, case_insensitive=True, help_command=None, allowed_mentions=discord.AllowedMentions(replied_user=False))


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


initial_cogs = [
    "jishaku",
    "cogs.error_handler"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@bot.event
async def on_ready():
    logging.info(f"Bot has successfully launched as {bot.user}")


bot.run(os.getenv("TOKEN"))
