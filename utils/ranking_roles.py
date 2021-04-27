import logging
from discord.ext import commands
from firebase_admin import firestore


rankings = {
    "Bronze": (0,9,"835882077298622465"),
    "Silver": (10,25,"835882144169590814"),
    "Gold": (26,45,"835882146048376853"),
    "Platinum": (46,60,"835882148539924490"),
    "Diamond": (61,75,"835882150909050900"),
    "Master": (76,float("inf"),"835882152490434560"),
}


async def determine_rank(ctx):
    logging.info("determine_rank invoked")
    dab = firestore.client()
    mp = int(dab.collection("users").document(str(ctx.author.id)).get().get("MP"))
    for x in rankings:
        if rankings[x][0] <= mp <= rankings[x][1]:
            logging.info(f"returned {x}")
            return x



async def assign_rank(ctx):
    logging.info("assign_rank invoked")
    dab = firestore.client()
    new_rank = await determine_rank(ctx)
    current_rank = dab.collection("users").document(str(ctx.author.id)).get().get("rank")
    if new_rank == current_rank:
        return
    await ctx.author.remove_roles(await commands.RoleConverter().convert(ctx, rankings[current_rank][2]))
    await ctx.author.add_roles(await commands.RoleConverter().convert(ctx, rankings[new_rank][2]))
    dab.collection("users").document(str(ctx.author.id)).update({"rank": new_rank})

async def rank_list():
    logging.info("rank_list inoked")
    message = str()
    for x in rankings:
        message = message+f"**{x}**: {rankings[x][0]} - {rankings[x][1]}\n"
    return message