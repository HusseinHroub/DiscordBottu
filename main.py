# Discord bot V1

import discord
import os
import Commands.CommandsFactory as CommandsFactory
from keep_alive import keep_alive
import shlex
import traceback
from Jobs.JobScheduler import JobScheduler
import sotrageutils
from Jobs.Tasks.LolStatUpdatorTask import LolStatUpdatorTask
from Jobs.Tasks.LolAnnouncer import LolAnnouncer
import asyncio

client = discord.Client()

botChannelId = 641925086055628801


def stringStringArray(stringArray):
    for i in range(len(stringArray)):
        stringArray[i] = stringArray[i].strip()


@client.event
async def on_ready():
    sotrageutils.updateCache()
    print('Updated cache')
    JobScheduler(LolAnnouncer(client.get_channel(botChannelId),
                              asyncio.get_running_loop()), 3600).start()
    JobScheduler(LolStatUpdatorTask(client.get_channel(botChannelId),
                                    asyncio.get_running_loop()), 300).start()
    print('started two jobs bro!')


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
            embed = discord.Embed(description=embedDescrption, color=0x27966b)
            await message.channel.send(embed=embed)


keep_alive()
client.run(os.getenv('CTOKEN'))
