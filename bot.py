import discord
import os
import latex

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$latex'):
        input_expr = message.content.split(None, 1)[1]
        png = latex.GeneratePNGFromExpression(input_expr)
        if png is not None:
            await message.channel.send(file=discord.File(png, 'image.png'))

client.run(os.getenv('DISCORD_TOKEN'))