import dbutils
import cacheutils


def updateCache():
  topKills = dbutils.getSummonersSortedByStat('kills')
  topDeaths = dbutils.getSummonersSortedByStat('deaths', False)
  topAssists = dbutils.getSummonersSortedByStat('assists')
  topAvgKda = dbutils.getSummonersSortedByStat('avg_kda')
  topFarms = dbutils.getSummonersSortedByStat('farms')
  topTotalGames = dbutils.getSummonersSortedByStat('total_games')
  cacheutils.updateSortedLists(topKills, topDeaths, topAssists, topAvgKda, topFarms, topTotalGames)
 
def getSummonersSortedByStat(statType):
  return cacheutils.getSummonersSortedByStat(statType)

def getRecentTopPlayer():
  return dbutils.getRecentTopPlayer()

def getKDAList():
  return cacheutils.getKDAList()

def updateRecentTopPlayer(summonerName):
  dbutils.updateRecentTopPlayer(summonerName)