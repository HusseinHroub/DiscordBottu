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
from lolutils import constants
from requestUtls import utils

client = discord.Client()

botChannelId = int(os.getenv('BOT_CHANNEL_ID'))
GREEN = 0x27966b
RED = 0xff3d3d
STAT_UPDATER_PERIOD = 60

def stripStringArray(stringArray):
    for i in range(len(stringArray)):
        stringArray[i] = stringArray[i].strip()


@client.event
async def on_ready():
    updateCaches()
    JobScheduler(LolStatUpdatorTask(client.get_channel(botChannelId),
                                    asyncio.get_running_loop()), STAT_UPDATER_PERIOD).start()
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
        if message.channel.id != botChannelId and messageContent.lower() != '!leave':
            apology = f'Sorry I only work in <#{botChannelId}> channel :('
            embed = discord.Embed(description=apology, color=RED)
            await message.channel.send(embed=embed)
            return

        embedColor = GREEN
        embed_result = True
        try:
            fullCommand = shlex.split(messageContent)
            stripStringArray(fullCommand)
            command = CommandsFactory.getCommand(fullCommand[0])
            result = command.execute(fullCommand[1:])
            result_array = result.result_array
            embed_result = result.embed_result
        except Exception as e:
            result_array = [str(e)]
            embedColor = RED
            traceback.print_exc()
        if len(result_array) > 0:
            await send_result_to_channel(embedColor, embed_result, message.channel, result_array)


async def send_result_to_channel(embedColor, embed_result, channel, result_array):
    for result in result_array:
        if result != '':
            if embed_result:
                embed = discord.Embed(description=result, color=embedColor)
                await channel.send(embed=embed)
            else:
                await channel.send(result)


client.run(os.getenv('CTOKEN'))
