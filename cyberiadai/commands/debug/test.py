from discord.ext import commands

@commands.command()
async def test(ctx):
    """Counts up the number of messages the user has posted in the previous 100 messages of the channel"""
    counter = 0
    tmp = await ctx.channel.send('Calculating messages...')
    async for log in ctx.channel.history(limit=100):
        if log.author == ctx.author:
            counter += 1
    await tmp.edit(content='You have {} messages.'.format(counter))
