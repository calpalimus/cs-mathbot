import discord
import os
import graphics

import parser

from parser.interpreter import RunBotCommand
from parser.latex import ParseTreeToLaTeX

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        result = RunBotCommand(message.content)
        if isinstance(result, discord.File):
            await message.channel.send(file=result)
        else:
            await message.channel.send(result)

client.run(os.getenv('DISCORD_TOKEN'))