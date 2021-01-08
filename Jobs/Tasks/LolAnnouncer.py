import cacheutils
import discord
import asyncio
class LolAnnouncer:
  
  def __init__(self, channel, loop):
    self.channel = channel
    self.recentTopSummoner = None
    self.loop = loop

  def execute(self):
    topSummoner = cacheutils.getKDAList()[0]
    if self.recentTopSummoner == None or topSummoner[0] != self.recentTopSummoner[0]:
      self.recentTopSummoner = topSummoner
      embed=discord.Embed(description=f'{self.recentTopSummoner[0]} is the top summoner with {self.recentTopSummoner[1]} kda, good job!.', color=0x27966b)
      print('added to mainm loop')
      asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)
