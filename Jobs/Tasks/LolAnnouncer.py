import cacheutils
import discord

class LolAnnouncer:
  
  def __init__(self, channel, loop):
    self.channel = channel
    self.recentTopSummoner = None
    self.loop = loop

  def execute(self):
    topSummoner = cacheutils.getKDAList()[0]
    if topSummoner != self.recentTopSummoner:
      self.recentTopSummoner = topSummoner
      embed=discord.Embed(description=f'{self.recentTopSummoner[0]} is the top summoner with {self.recentTopSummoner[1]} kda, good job!.', color=0x27966b)
      self.loop.create_task(self.channel.send(embed=embed))
