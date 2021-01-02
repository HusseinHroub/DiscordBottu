import dbutils

class SimpleTopListExtractor:
   def __init__(self, statType):
    self.statType = statType

   def extract(self):
     summoners_data = dbutils.getSummonersSortedByStat(self.statType, self.statType != 'deaths')
     response = ''
     counter = 1
     for summoner_data in summoners_data:
       response = response + f'{counter}- {summoner_data[0]} with {summoner_data[1]} {self.statType}\n'
       counter = counter + 1
     return response