import discord
import logging
import asyncio
from discord.ext import commands
from discord.ext.commands.errors import BadArgument
from firebase_admin import firestore

dab = firestore.client()
matches = dict()


class MultiRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def matchstart(self, ctx, *members:discord.Member):
        logging.info(f"matchstart invoked by {ctx.author.name} with {members}")
        global matches
        if ctx.author.id in matches.keys():
            return await ctx.send("You've already got an open match!")
        players = list()
        y = str()
        col_ref = dab.collection("users").document("collectionlist").get().get('array')
        for x in members:
            if str(x.id) not in col_ref:
                return await ctx.send(f"{x.name} isn't registered!")
            players.append(x.name)
            if x == members[-1]:
                y = y[:-2]+" and "+x.name
                break
            y = y+x.name+", "
        if len(players) < 2:
            return await ctx.send("You can't start a match by yourself!")
        elif len(players) != len(set(players)):
            raise BadArgument
        await ctx.send(f"Match starting between {y}!")
        del y
        matches.update({ctx.author.id: players})
        for x in members:
                if x == ctx.author:
                    continue
                message = await ctx.send(f"{x.mention} Do you accept the match?")
                await message.add_reaction('✅')
                await message.add_reaction('❌')
                def check(reaction, user): # Me stealing code from the discord.py server B)
                    return str(reaction.emoji) in ['✅', '❌'] and user == x
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send(f"{x.name} didn't react in time! match cancelled")
                else:
                    if str(reaction.emoji) == '✅':
                        continue
                    if str(reaction.emoji) == '❌':
                        return await ctx.send(f"{x.name} declined. match cancelled")
        await ctx.send(f"{ctx.author.name}'s match has started!\ngl hf B)")
        logging.info(f"Match successfully started. Current matches: {matches}")
                        

    @commands.command()
    async def matchend(self, ctx):
        logging.info(f"matchend invoked by {ctx.author.name}")
        global matches
        await ctx.send(matches)


def setup(bot):
    bot.add_cog(MultiRanking(bot))
