# Discord bot V3

import asyncio
import os
import shlex
import traceback

import discord

import Commands.CommandsFactory as CommandsFactory
import sotrageutils
from Jobs.JobScheduler import JobScheduler
from Jobs.Tasks.LolStatUpdatorTask import LolStatUpdatorTask
from dbutils import SessionManager
from keep_alive import keep_alive
from lolutils import constants
from requestUtls import utils

client = discord.Client()

botChannelId = int(os.getenv('BOT_CHANNEL_ID'))


def stripStringArray(stringArray):
    for i in range(len(stringArray)):
        stringArray[i] = stringArray[i].strip()


@client.event
async def on_ready():
    updateCaches()
    # JobScheduler(LolAnnouncer(client.get_channel(botChannelId),
    #                           asyncio.get_running_loop()), 3600).start()
    JobScheduler(LolStatUpdatorTask(client.get_channel(botChannelId),
                                    asyncio.get_running_loop()), 300).start()
    print('started two jobs bro!')
    initChampionData()
    print('initialized champion data')


@SessionManager
def updateCaches(session):
    sotrageutils.updateStatCache(session)
    sotrageutils.updateAnnouncedMonthValue(session)
    print('Updated cache')

def initChampionData():
    champ_data = utils.getHTTPJsonResponse('http://ddragon.leagueoflegends.com/cdn/11.2.1/data/en_US/champion.json')
    data = champ_data['data']
    keys = data.keys()
    my_format = {}
    for key in keys:
        val = data[key]
        my_format[val["key"]] = {
            "name": val["name"],
            "icon": val["image"]["full"]
        }
    constants.CHAMPIONS_DATA = my_format


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageContent = message.content
    if messageContent.startswith('!l') or messageContent.startswith('!L'):
        try:
            fullCommand = shlex.split(messageContent)
            stripStringArray(fullCommand)
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
