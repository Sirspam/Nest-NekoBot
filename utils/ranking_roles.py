import logging
from discord.ext import commands
from firebase_admin import firestore


rankings = {
    "Bronze": (0,9,"835216296223178762"),
    "Silver": (10,25,"835216378130333757"),
    "Gold": (26,45,"835216412065660928"),
    "Platinum": (46,60,"835216431334686752"),
    "Dimaond": (61,75,"835272527655338065"),
    "Master": (76,float("inf"),"835272554561404980"),
}


async def determine_rank(ctx):
    logging.info("determine_rank invoked")
    dab = firestore.client()
    MP = int(dab.collection("users").document(str(ctx.author.id)).get().get("MP"))
    for x in rankings:
        if rankings[x][0] <= MP <= rankings[x][1]:
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

