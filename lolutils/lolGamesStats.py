from lolutils import lolApiUtils
from queue import Queue
from threading import Thread

def getTotalStatsOfMatches(matches, accountId):
  results = getStatResultsFromWorkerThreads(matches, accountId)
  return calculateMergedStatsResults(results)
  
def getStatResultsFromWorkerThreads(matches, accountId):
  queue = Queue(maxsize=0)
  numberOfThreads = min(30, len(matches))
  results = [(0, 0, 0) for x in matches];
  for i in range(len(matches)):
    queue.put((i,matches[i]['gameId']))
  threads = []
  for i in range(numberOfThreads):
    worker = Thread(target=getTotalStatsOfMatchesWorker, args=(queue,accountId, results))
    threads.append(worker)
    worker.start()
  for worker in threads:
    worker.join()
  return results

def getTotalStatsOfMatchesWorker(queue, accountId, results):
  while not queue.empty():
    work = queue.get()
    kills, deaths, assists = lolApiUtils.getStatsOfGameId(work[1], accountId)
    results[work[0]]=(kills, deaths, assists)
    
def calculateMergedStatsResults(results):
  total_kills = 0
  total_deaths = 0
  total_assists = 0
  for result in results:
    total_kills += result[0]
    total_deaths += result[1]
    total_assists += result[2]
  return total_kills, total_deaths, total_assists