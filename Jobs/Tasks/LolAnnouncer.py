import cacheutils
class LolAnnouncer:
  
  def __init__(self, channel):
    self.channel = channel
    self.recentTopSummoner = None

  async def execute(self):
    topSummoner = cacheutils.getKDAList()[0]
    if topSummoner[0] != self.recentTopSummoner:
      self.recentTopSummoner = self.kdaList[0]
      await self.channel.send(f'{self.recentTopSummoner[0]} is the top summoner with {self.recentTopSummoner[1]} kda, good job!.')

