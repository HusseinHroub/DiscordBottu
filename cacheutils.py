import threading
# import time

# lock = threading.Lock()

topKills = []
topDeaths = []
topAssists = []
topKdas = []


def getSummonersSortedByStat(stats):
  return doGetSummonerSortedByStat(stats)

def doGetSummonerSortedByStat(stats):
  switch = {
    'kills' : topKills,
    'deaths' : topDeaths,
    'assists' : topAssists,
    'kda' : topKdas
    }

  response = switch.get(stats)
  if response == None:
    raise Exception(f"couldn't find stats type of {stats}")
  return response

def updateSortedLists(newTopKills, newTopDeaths, newTopAssists, newTopKdas):
  global topKills
  global topDeaths
  global topAssists
  global topKdas

  topKills = newTopKills
  topDeaths = newTopDeaths
  topAssists = newTopAssists
  topKdas = newTopKdas
