import cacheutils
import dbutils
from statsUtils import stat_helper_utils


@dbutils.SessionManager
def updateStatCache(session):
    for statHelper in stat_helper_utils.stat_helpers:
        statHelper.updateCache(session)


def getSummonersSortedByStat(statType):
    return cacheutils.getSummonersSortedByStat(statType)


@dbutils.SessionManager
def getRecentTopPlayer(session):
    return dbutils.getCommonTableValue('recentTopSummoner', session)


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
    cacheutils.markMonthAnnouncedValue(dbutils.getCommonTableValue('monthAnnouncedValue', session))
