from queue import Queue
from threading import Thread

from lolutils import lolApiUtils, constants


def getTotalStatsOfMatches(matches, accountId):
    if matches == None or len(matches) == 0:
        print('wanring, got empty matches array')
        return []
    results = getStatResultsFromWorkerThreads(matches, accountId)
    throwIfResultContainNone(results)
    filtered_results = filterResultsForUnneeddedQueueIds(results)
    return filtered_results


def getStatResultsFromWorkerThreads(matches, accountId):
    queue = Queue(maxsize=0)
    numberOfThreads = 1
    results = [None for x in matches]
    for i in range(len(matches)):
        queue.put((i, matches[i]))
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


def filterResultsForUnneeddedQueueIds(results):
    filterred_results = []
    for result in results:
        if result['queueId'] not in constants.BLACK_LISTED_QUEUE_IDS:
            filterred_results.append(result)
    return filterred_results
