import discord
import os
import Commands.CommandsFactory as CommandsFactory
from keep_alive import keep_alive
import shlex
import traceback
from Jobs import statsUpdatorJob
import sotrageutils
client = discord.Client()

def stringStringArray(stringArray):
  for i in range (len(stringArray)):
        stringArray[i] = stringArray[i].strip()

@client.event
async def on_ready():
  print('Hello bot is ready')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
   
  messageContent = message.content
  if messageContent.startswith('!l') or messageContent.startswith('!L'):
    try:
      fullCommand = shlex.split(messageContent)
      stringStringArray(fullCommand)
      command = CommandsFactory.getCommand(fullCommand[0], fullCommand[1:])
      embedDescrption = command.execute()
    except Exception as e:
      embedDescrption = 'Error happened: ' + str(e)
      traceback.print_exc()
    if embedDescrption != None and embedDescrption != '':
      embed=discord.Embed(description=embedDescrption, color=0x27966b)
      await message.channel.send(embed=embed)
  
keep_alive()
sotrageutils.updateCache()
statsUpdatorJob.start()
client.run(os.getenv('CTOKEN'))