import dbutils
import cacheutils


def updateCache():
  topKills = dbutils.getSummonersSortedByStat('kills')
  topDeaths = dbutils.getSummonersSortedByStat('deaths', False)
  topAssists = dbutils.getSummonersSortedByStat('assists')
  topKdas = dbutils.getSummonersSortedByStat('kda')
  cacheutils.updateSortedLists(topKills, topDeaths, topAssists, topKdas)
 
def getSummonersSortedByStat(statType):
  return cacheutils.getSummonersSortedByStat(statType)