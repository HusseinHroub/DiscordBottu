import requests
import os
from ratelimit import limits, sleep_and_retry
from queue import Queue
from threading import Thread

region = 'euw1'
api_key = os.getenv('LAPIKEY')
root_url = f'https://{region}.api.riotgames.com/lol'

CALLS_NUMBER = 100
CALLS_PERIOD = 120

threadCounterCalls = 0
@sleep_and_retry
@limits(calls=CALLS_NUMBER, period=CALLS_PERIOD)
def getJsonResponseOfUrl(url):
  global threadCounterCalls
  threadCounterCalls += 1
  print(f"threadCounterCalls: {threadCounterCalls}")
  response = requests.get(url)
  if response.status_code != 200 and response.status_code != 404:
    raise Exception(f'While trying to get url request, got the following response code: {response.status_code}')
  elif response.status_code == 404:
    return None
  return response.json()

def getAccountIdByName(name):
  jsonResponse = getJsonResponseOfUrl(f'{root_url}/summoner/v4/summoners/by-name/{name}?api_key={api_key}')
  if jsonResponse == None:
    raise Exception(f"Couldn't find summoner with name: {name}")
  return jsonResponse['accountId']


def getMatchesByAccountId(accountId, beginTime=0):
  jsonResponse = getJsonResponseOfUrl(f'{root_url}/match/v4/matchlists/by-account/{accountId}?api_key={api_key}&beginTime={beginTime}')
  return None if jsonResponse == None else jsonResponse['matches']
  
    

def getParticpantIdOfGameDetails(match_details, accountId):
  participantIdentities = match_details['participantIdentities']
  for participantIdentity in participantIdentities:
    if participantIdentity['player']['accountId'] == accountId:
      return participantIdentity['participantId']
  return -1


def getStatsOfGameId(gameId, accountId):
  match_details = getJsonResponseOfUrl(f'{root_url}/match/v4/matches/{gameId}?api_key={api_key}')
  particpantId = getParticpantIdOfGameDetails(match_details, accountId)
  if particpantId != -1:
    stats =match_details['participants'][particpantId - 1]['stats'] 
    return stats['kills'], stats['deaths'], stats['assists']
  else:
    print(f'warning cloudnt find particpantId of gameId: {gameId}')
    return 0

def getTotalStatsOfMatches(matches, accountId):
  print('started working bro')
  print('matches length')
  print(len(matches))
  q = Queue(maxsize=0)
  num_theads = min(3, len(matches))
  results = [{} for x in matches];
  for i in range(len(matches)):
    q.put((i,matches[i]['gameId']))
  threads = []
  for i in range(num_theads):
    worker = Thread(target=getTotalStatsOfMatchesWorker, args=(q,accountId, results))
    threads.append(worker)
    worker.start()
  print('before join')
  for worker in threads:
    worker.join()
  print('after join')
  total_kills = 0
  total_deaths = 0
  total_assists = 0
  for result in results:
    total_kills += result[0]
    total_deaths += result[1]
    total_assists += result[2]
  print('finished working bro')
  return total_kills, total_deaths, total_assists
  
def getTotalStatsOfMatchesWorker(queue, accountId, results):
  while not queue.empty():
    work = queue.get()
    kills, deaths, assists = getStatsOfGameId(work[1], accountId)
    results[work[0]]=(kills, deaths, assists)
