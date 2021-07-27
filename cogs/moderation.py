import logging
from datetime import datetime
from re import findall

from discord import User, Embed, Colour, File

from discord.ext import commands
from utils.role_checks import moderator_check, on_message_mod_check
from utils.logger import log_info


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author.bot is True:
            return
        # Self-promo
        if message.channel.id == 587966826856841226 and not findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",message.content) and not await on_message_mod_check(await self.bot.get_context(message)):
            logging.info(f"Deleting message in #self-promo by {message.author.name}:\n{message.content}")
            await message.delete()
            await message.author.send("No discussion in self-promo :tf:", file=File(self.bot.cwd+"/assets/bog_off_wanker.png"))
            await log_info(self, ("Deleted message in #self-promo",f"{message.author.name}:\n{message.content}"))

    @commands.command()
    @moderator_check()
    async def ban(self, ctx, user:User, *, reason = None):
        logging.info(f"Banning {user.name} for '{reason}' by {ctx.author.name}")
        if reason is None:
            reason = "No reason was given"
        await user.send(embed=Embed(
            title=f"You've been banned from {ctx.guild.name}",
            description=f"{reason}\n\n[Click here to make an unban request](https://forms.gle/zYVHijTdzBU6itX46 )",
            timestamp=datetime.utcnow(),
            colour=Colour.red()
        ), file=File(self.bot.cwd+"/assets/bog_off_wanker.png"))
        await ctx.guild.ban(user, reason=reason)
        await ctx.reply(f"Bogged off the wanker :tf:\n``banned {user.name}``")
        await log_info(self, (f"Banned {ctx.user}",f"Banned by {ctx.author.name} for {reason}"))

def setup(bot):
    bot.add_cog(Moderation(bot))