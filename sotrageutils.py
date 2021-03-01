import cacheutils
import dbutils


def updateStatCache():
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
    return dbutils.getCommonTableRow('recentTopSummoner')


def getTopKillsList():
    return cacheutils.topKills


def getTopDeathsList():
    return cacheutils.topDeaths


def getTopAssistsList():
    return cacheutils.topAssists


def getTopFarmsList():
    return cacheutils.topFarms


def getTopGamesList():
    return cacheutils.topTotalGames


def getTopKDAList():
    return cacheutils.topAvgKda


def updateRecentTopPlayer(summonerName):
    dbutils.updateCommonTableRow('recentTopSummoner', summonerName)


def getMonthAnnouncedValue():
    return cacheutils.monthAnnounceValue


def markMonthAnnouncedValue(new_value):
    dbutils.updateCommonTableRow('monthAnnouncedValue', new_value)
    cacheutils.markMonthAnnouncedValue(new_value)


def updateAnnouncedMonthValue():
    cacheutils.markMonthAnnouncedValue(dbutils.getCommonTableRow('monthAnnouncedValue'))
