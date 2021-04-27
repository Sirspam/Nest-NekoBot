import logging
from discord.ext import commands
from firebase_admin import firestore


rankings = {
    #Name: min MP, max MP, role ID, emote ID
    "Bronze": (0,9,"835882077298622465","<:Bronze:836531324348530699>"),
    "Silver": (10,25,"835882144169590814","<:Silver:836531344963272744>"),
    "Gold": (26,45,"835882146048376853","<:Gold:836531357646716928>"),
    "Platinum": (46,60,"835882148539924490","<:Platinum:836531372436619274>"),
    "Diamond": (61,75,"835882150909050900","<:Diamond:836531381592129537>"),
    "Master": (76,float("inf"),"835882152490434560","<:Master:836531391423709195>"),
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
        if rankings[x][1] == float("inf"):
            message = message+f"{rankings[x][3]} **{x}**: {rankings[x][0]}+"
        else:
            message = message+f"{rankings[x][3]} **{x}**: {rankings[x][0]} - {rankings[x][1]}\n"
    return message