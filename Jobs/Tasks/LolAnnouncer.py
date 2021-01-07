class LolAnnouncer:
  
  def __init__(self, channel, kdaList):
    self.channel = channel
    self.kdaList = kdaList
    self.recentTopSummoner = None

  async def execute(self):
    topSummoner = self.kdaList[0]
    if topSummoner[0] != self.recentTopSummoner:
      self.recentTopSummoner = self.kdaList[0]
      await self.channel.send(f'{self.recentTopSummoner[0]} is the top summoner with {self.recentTopSummoner[1]} kda, good job!.')

