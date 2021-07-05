from jishaku import Jishaku, Feature
from discord.ext.commands import Context, MissingPermissions

DEVS = [232574143818760192, 451495805451239426]

async def cog_check_patch(self: Feature, ctx: Context):
    if ctx.author.guild_permissions.administrator is True or "587963873186021376" in str(ctx.author.roles): 
        return True
    raise MissingPermissions("Moderator role")

Jishaku.cog_check = cog_check_patch