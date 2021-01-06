import dbutils
import enum

class ModeTypes(enum.Enum):
  top = 0
  worst = 1

class SimpleSortedListExtractor:
   def __init__(self, modeType, statType):
    self.modeType = modeType
    self.statType = statType

   def extract(self):
     summoners_data = dbutils.getSummonersSortedByStat(self.statType, self.getSortingOrder())
     response = ''
     counter = 1
     for summoner_data in summoners_data:
       response = response + f'{counter}- {summoner_data[0]} with {summoner_data[1]} {self.statType}\n\n'
       counter = counter + 1
     return response


   def getSortingOrder(self):
     if self.modeType == ModeTypes.top:
       return self.statType != 'deaths'
     else:
       return self.statType == 'deaths'