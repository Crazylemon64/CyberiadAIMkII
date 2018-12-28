from discord.ext import commands

@commands.command()
async def status(ctx):
    await ctx.channel.send("Send server status [NYI]")
