import sotrageutils
import discord
import asyncio
class LolAnnouncer:
    
  def __init__(self, channel, loop):
    self.channel = channel
    self.loop = loop

  def execute(self):
    topSummoner = sotrageutils.getKDAList()[0]
    recentTopSummonerName = sotrageutils.getRecentTopPlayer()
    if recentTopSummonerName == None or topSummoner[0] != recentTopSummonerName[0]:
      recentTopSummonerName = topSummoner[0]
      embed=discord.Embed(description=f'{recentTopSummonerName} is the top summoner with {topSummoner[1]} kda, good job!.', color=0x27966b)
      asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)
      sotrageutils.updateRecentTopPlayer(recentTopSummonerName)
      print('updated')
