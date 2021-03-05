import cacheutils
import dbutils


@dbutils.SessionManager
def updateStatCache(session):
    topKills = dbutils.getSummonersSortedByStat('kills', True, session)
    topDeaths = dbutils.getSummonersSortedByStat('deaths', False, session)
    topAssists = dbutils.getSummonersSortedByStat('assists', True, session)
    topAvgKda = dbutils.getSummonersSortedByStat('avg_kda', True, session)
    topFarms = dbutils.getSummonersSortedByStat('farms', True, session)
    topTotalGames = dbutils.getSummonersSortedByStat('total_games', True, session)
    cacheutils.updateSortedLists(topKills, topDeaths, topAssists, topAvgKda, topFarms, topTotalGames)


def getSummonersSortedByStat(statType):
    return cacheutils.getSummonersSortedByStat(statType)


@dbutils.SessionManager
def getRecentTopPlayer(session):
    return dbutils.getCommonTableRow('recentTopSummoner', session)


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


@dbutils.SessionManager
def updateRecentTopPlayer(summonerName, session):
    dbutils.updateCommonTableRow('recentTopSummoner', summonerName, session)


def getMonthAnnouncedValue():
    return cacheutils.monthAnnounceValue


@dbutils.SessionManager
def markMonthAnnouncedValue(new_value, session):
    dbutils.updateCommonTableRow('monthAnnouncedValue', new_value, session)
    cacheutils.markMonthAnnouncedValue(new_value)


@dbutils.SessionManager
def updateAnnouncedMonthValue(session):
    cacheutils.markMonthAnnouncedValue(dbutils.getCommonTableRow('monthAnnouncedValue', session))
