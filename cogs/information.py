from discord import Embed, Colour

from discord.ext import commands


class Information(commands.Cog):
    "Informational related commands "
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["invite"], help="Posts links relevant to the bot")
    async def links(self, ctx):
        embed = Embed(
            description=
f"""[**Home Server**](https://discord.gg/zTCJh8H)
[**Github Repo**]({self.bot.github_repo})\n
I hope you're having a good day :)""",
            color= Colour.red())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/765183849876684810.gif?v=1")
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))