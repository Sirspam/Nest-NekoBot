from discord.abc import GuildChannel
from discord.utils import get
from discord.ext import commands


async def on_message_mod_check(ctx):
    if ctx.author.guild_permissions.administrator or get(ctx.author.roles, id=587963873186021376):
        return True
    return False

def moderator_check():
    async def predicate(ctx):
        if not isinstance(ctx.channel, GuildChannel):
            raise commands.NoPrivateMessage
        if ctx.author.guild_permissions.administrator or get(ctx.author.roles, id=587963873186021376):
            return True
        raise commands.MissingPermissions("Moderator")
    return commands.check(predicate)