import discord
import os
import Commands.CommandsFactory as CommandsFactory
from keep_alive import keep_alive


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
      fullCommand = message.content.split()
      command = CommandsFactory.getCommand(fullCommand[0], fullCommand[1:])
      response = command.execute()
    except Exception as e:
      response = e
    if response != '':
      await message.channel.send(response)

    


keep_alive()
client.run(os.getenv('CTOKEN'))