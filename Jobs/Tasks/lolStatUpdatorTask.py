import dbutils
from lolutils import lolApiUtils
from queue import Queue
from threading import Thread
import time

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
    results[work[0]]={'kills': 0, 'deaths': 0, 'assists': 0, 'accountId': summonerData[0], 'lastGameTimeStamp': time.time()}
    matches = lolApiUtils.getMatchesByAccountId(summonerData[0], summonerData[4])
    if matches != None and len(matches) > 0:
      kills, deaths, assists = lolApiUtils.getTotalStatsOfMatches(matches, summonerData[0])
      result = results[work[0]]
      result['kills'] = kills
      result['deaths'] = deaths
      result['assists'] = assists
      result['lastGameTimeStamp'] = matches[0]['timestamp'] + 1
    
def getNewSummonerData(summonersData, results):
  newSummonersData = []
  for i in range(len(summonersData)):
    if(results[i][0] == 0 and results[i][1] == 0 and results[i][2] == 0):
      continue
    result = results[i]
    summonerData = summonersData[i]
    newSummonersData.append({
      'kills': result['kills'] + summonerData[1],
      'deaths': result['deaths'] + summonerData[2],
      'assists': result['assists'] + summonerData[3],
      'accountId': result['accountId'],
      'lastGameTimeStamp': result['lastGameTimeStamp']
    })
  return newSummonersData
  
def updateToDBIfNotEmptyData(newSummonersData):
  if newSummonersData != None and len(newSummonersData) > 0:
    print('updating db!')
    dbutils.updateSummonersData(newSummonersData)