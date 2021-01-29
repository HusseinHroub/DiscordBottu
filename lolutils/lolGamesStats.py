from queue import Queue
from threading import Thread

from lolutils import lolApiUtils


def getTotalStatsOfMatches(matches, accountId):
    if matches == None or len(matches) == 0:
        print('wanring, got empty matches array')
        return []
    results = getStatResultsFromWorkerThreads(matches, accountId)
    throwIfResultContainNone(results)
    return results


def getStatResultsFromWorkerThreads(matches, accountId):
    queue = Queue(maxsize=0)
    numberOfThreads = min(30, len(matches))
    results = [None for x in matches];
    for i in range(len(matches)):
        queue.put((i, matches[i]['gameId']))
    threads = []
    for i in range(numberOfThreads):
        worker = Thread(target=getTotalStatsOfMatchesWorker, args=(queue, accountId, results))
        threads.append(worker)
        worker.start()
    for worker in threads:
        worker.join()
    return results


def getTotalStatsOfMatchesWorker(queue, accountId, results):
    while not queue.empty():
        work = queue.get()
        stats = lolApiUtils.getStatsOfGameId(work[1], accountId)
        results[work[0]] = stats


def throwIfResultContainNone(results):
    for result in results:
        if result == None:
            raise Exception("Had none result for this atmoic opereation.")
