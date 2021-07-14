from datetime import datetime

from discord import Embed, Colour


async def log_info(self, content):
    await self.bot.logger_channel.send(embed=Embed(
        title=f"INFO: {content[0]}",
        description=content[1],
        timestamp=datetime.utcnow(),
        colour=Colour.blue()
    ))

async def log_warning(self, content):
    await self.bot.logger_channel.send(embed=Embed(
        title=f"WARNING: {content[0]}",
        description=content[1],
        timestamp=datetime.utcnow(),
        colour=Colour.orange()
    ))

async def log_error(self, content):
    await self.bot.logger_channel.send(embed=Embed(
        title=f"ERROR: {content[0]}",
        description=content[1],
        timestamp=datetime.utcnow(),
        colour=Colour.red()
    ))