import dbutils
from lolutils import lolApiUtils
from queue import Queue
from threading import Thread

def updateDBStats():
  summonersData = dbutils.getAllSummonerData()
  print('got summoners data')
  results = getSummonersStats(summonersData)
  print('got summoners results')
  newSummonersData = getNewSummonerData(summonersData, results)
  print('merged results')
  updateToDBIfNotEmptyData(newSummonersData)

def getSummonersStats(summonersData):
  queue = Queue(maxsize=0)
  numberOfThreads = min(30, len(summonersData))
  results = [{} for x in summonersData];
  for i in range(len(summonersData)):
    queue.put((i, summonersData[i]))
  threads = []
  for i in range(numberOfThreads):
    worker = Thread(target=getTotalStatsOfSummonerWorker, args=(queue, results))
    threads.append(worker)
    worker.start()
  for worker in threads:
    worker.join()
  return results

def getTotalStatsOfSummonerWorker(queue, results):
  while not queue.empty():
    work = queue.get()
    summonerData = work[1]
    results[work[0]]={'kills': 0, 'deaths': 0, 'assists': 0, 'accountId': summonerData[0]}
    games = lolApiUtils.getMatchesByAccountId(summonerData[0], summonerData[4])
    if games != None and len(games) > 0:
      kills, deaths, assists = lolApiUtils.getTotalStatsOfMatches(games, summonerData[0])
      result = results[work[0]]
      result['kills'] = kills
      result['deaths'] = deaths
      result['assists'] = assists
    
def getNewSummonerData(summonersData, results):
  newSummonersData = []
  for i in (len(summonersData)):
    if(results[i][0] == 0 and results[i][1] == 0 and results[i][2] == 0):
      continue
    newSummonersData.append({
      'kills': results[i]['kills'] + summonersData[i][1],
      'deaths': results[i]['deaths'] + summonersData[i][2],
      'assists': results[i]['deaths'] + summonersData[i][3],
      'accountId': results[i]['accountId']
    })
  return newSummonersData
  
def updateToDBIfNotEmptyData(newSummonersData):
  if newSummonersData != None and len(newSummonersData) > 0:
    print('updating db!')
    dbutils.updateSummonersData(newSummonersData)