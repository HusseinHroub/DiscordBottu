import dbutils

class SimpleRankExtractor:
   def __init__(self, statType):
    self.statType = statType

   def extract(self, summonerName):
     summoners_data = dbutils.getSummonersSortedByStat(self.statType, self.statType != 'deaths')
     counter = 0
     for summoner_data in summoners_data:
       counter = counter + 1
       if summoner_data[0] == summonerName:
         return f"{summonerName} {self.statType} rank is {counter}, total {self.statType}: {summoner_data[1]}"
     return 'Sorry, wasnt able to locate summoner name'