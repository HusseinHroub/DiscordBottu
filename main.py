import discord
import os
from keep_alive import keep_alive


client = discord.Client()

@client.event
async def on_ready():
  print('Hello bot is ready')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!'):
    await message.channel.send('Hello xD')


keep_alive()
client.run(os.getenv('CTOKEN'))