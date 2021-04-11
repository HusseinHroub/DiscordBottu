topKills = []
topDeaths = []
topAssists = []
topAvgKda = []
topFarms = []
topTotalGames = []
topWinsRate = []
monthAnnounceValue = False


def getSummonersSortedByStat(stats):
    return doGetSummonerSortedByStat(stats)


def doGetSummonerSortedByStat(stats):
    switch = {
        'kills': topKills,
        'deaths': topDeaths,
        'assists': topAssists,
        'avg_kda': topAvgKda,
        'farms': topFarms,
        'total_games': topTotalGames,
        'win_rate': topWinsRate
    }

    response = switch.get(stats)
    if response == None:
        raise Exception(f"couldn't find stats type of {stats}")
    return response


def updateSortedLists(newTopKills,
                      newTopDeaths,
                      newTopAssists,
                      newTopAvgKda,
                      newTopFarms,
                      newTopTotalGames,
                      newTopWinsRate):
    global topKills
    global topDeaths
    global topAssists
    global topAvgKda
    global topFarms
    global topTotalGames
    global topWinsRate

    topKills = newTopKills
    topDeaths = newTopDeaths
    topAssists = newTopAssists
    topAvgKda = newTopAvgKda
    topFarms = newTopFarms
    topTotalGames = newTopTotalGames
    topWinsRate = newTopWinsRate


def markMonthAnnouncedValue(new_value):
    global monthAnnounceValue
    monthAnnounceValue = new_value
