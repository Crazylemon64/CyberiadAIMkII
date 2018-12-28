from discord.ext import commands
from discord import channel

@commands.command(hidden=True)
@commands.is_owner()
async def dumpserverinfo(ctx):
    for s in ctx.bot._connection.guilds:
        ctx.bot.log.info("Server ({}, {})".format(s.name, s.id))
        for c in s.channels:
            ctx.bot.log.info("\t{}".format(repr(c)))
            if type(c) in [channel.TextChannel, channel.GroupChannel]:
                ctx.bot.log.info("\t\tTopic - {}".format(c.topic))
    await ctx.channel.send("Dumped server information to the bot's log")
