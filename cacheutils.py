import threading

# import time

# lock = threading.Lock()

topKills = []
topDeaths = []
topAssists = []
topAvgKda = []
topFarms = []
topTotalGames = []


def getSummonersSortedByStat(stats):
    return doGetSummonerSortedByStat(stats)


def doGetSummonerSortedByStat(stats):
    switch = {
        'kills': topKills,
        'deaths': topDeaths,
        'assists': topAssists,
        'avg_kda': topAvgKda,
        'farms': topFarms,
        'total_games': topTotalGames
    }

    response = switch.get(stats)
    if response == None:
        raise Exception(f"couldn't find stats type of {stats}")
    return response


def updateSortedLists(newTopKills, newTopDeaths, newTopAssists, newTopAvgKda, newTopFarms, newTopTotalGames):
    global topKills
    global topDeaths
    global topAssists
    global topAvgKda
    global topFarms
    global topTotalGames

    topKills = newTopKills
    topDeaths = newTopDeaths
    topAssists = newTopAssists
    topAvgKda = newTopAvgKda
    topFarms = newTopFarms
    topTotalGames = newTopTotalGames


def getKDAList():
    return topAvgKda
