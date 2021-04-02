import asyncio

import discord

import sotrageutils

#Not working as expected! check line 16, it returns the value not the tuple..
##Also, line 17 gets an object and not typle..... (cuz of the usage of sqlalchemy)
class LolAnnouncer:

    def __init__(self, channel, loop):
        self.channel = channel
        self.loop = loop

    def execute(self):
        topSummoner = sotrageutils.getTopKDAList()[0]
        recentTopSummonerName = sotrageutils.getRecentTopPlayer()
        if recentTopSummonerName == None or topSummoner[0] != recentTopSummonerName[0]:
            recentTopSummonerName = topSummoner[0]
            embed = discord.Embed(
                description=f'{recentTopSummonerName} is the top summoner with {topSummoner[1]} kda, good job!.',
                color=0x27966b)
            asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)
            sotrageutils.updateRecentTopPlayer(recentTopSummonerName)
            print('updated')
