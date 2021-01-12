from lolutils import lolApiUtils
from queue import Queue
from threading import Thread

def getTotalStatsOfMatches(matches, accountId):
  results = getStatResultsFromWorkerThreads(matches, accountId)
  return calculateMergedStatsResults(results)
  
def getStatResultsFromWorkerThreads(matches, accountId):
  queue = Queue(maxsize=0)
  numberOfThreads = min(30, len(matches))
  results = [None for x in matches];
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
    stats = lolApiUtils.getStatsOfGameId(work[1], accountId)
    results[work[0]]={
      'kills': stats['kills'],
      'deaths': stats['deaths'],
      'assists': stats['assists'],
      'totalMinionsKilled': stats['totalMinionsKilled'],
      'neutralMinionsKilled': stats['neutralMinionsKilled'],
      }
    
def calculateMergedStatsResults(results):
  total_kills = 0
  total_deaths = 0
  total_assists = 0
  total_farms = 0
  kda = 0.0
  sample_count = 0
  for result in results:
    if result != None:
      total_kills += result['kills']
      total_deaths += result['deaths']
      total_assists += result['assists']
      total_farms += result['totalMinionsKilled'] + result['neutralMinionsKilled']
      sample_count += 1
      kda += (result['kills'] + result['assists']) / (result['deaths'] if result['deaths'] > 0 else 1)
  avg_kda = 0.0
  if sample_count != 0:
    avg_kda = kda / sample_count
  return {
   'total_kills': total_kills,
   'total_deaths': total_deaths,
   'total_assists': total_assists, 
   'total_farms': total_farms,
   'avg_kda' : avg_kda,
   'sample_count': sample_count
   }