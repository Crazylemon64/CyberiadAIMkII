from discord.ext import commands
import asyncio

@commands.command()
async def sleep(ctx):
    """Sleeps for 5 seconds, and then prints a message"""
    await asyncio.sleep(5)
    await ctx.channel.send('Done sleeping')
