import discord
import os
import Commands.CommandsFactory as CommandsFactory
from keep_alive import keep_alive
import shlex
import traceback

client = discord.Client()

@client.event
async def on_ready():
  print('Hello bot is ready')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('!l'):
    try:
      fullCommand = shlex.split(message.content)
      command = CommandsFactory.getCommand(fullCommand[0], fullCommand[1:])
      response = command.execute()
    except Exception as e:
      response = 'Error happened: ' + str(e)
      traceback.print_exc()
    if response != '':
      await message.channel.send(response)

    


keep_alive()
client.run(os.getenv('CTOKEN'))