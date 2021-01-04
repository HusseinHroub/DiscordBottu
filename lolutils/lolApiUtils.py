import requests
import os
from ratelimit import limits, sleep_and_retry
from lolutils import lolGamesStats

region = 'euw1'
api_key = os.getenv('LAPIKEY')
root_url = f'https://{region}.api.riotgames.com/lol'

CALLS_NUMBER = 95
CALLS_PERIOD = 120

@sleep_and_retry
@limits(calls=CALLS_NUMBER, period=CALLS_PERIOD)
def getJsonResponseOfUrl(url):
  return doGetJsonResponseOfUrl(url)

@sleep_and_retry
@limits(calls=15, period=1)
def doGetJsonResponseOfUrl(url):
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
  jsonResponse = getJsonResponseOfUrl(f'{root_url}/match/v4/matchlists/by-account/{accountId}?api_key={api_key}&beginTime={beginTime}&endIndex=30')
  return None if jsonResponse == None else jsonResponse['matches']
  
    

def getParticpantIdOfGameDetails(match_details, accountId):
  participantIdentities = match_details['participantIdentities']
  for participantIdentity in participantIdentities:
    if participantIdentity['player']['currentAccountId'] == accountId:
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
  results = lolGamesStats.getStatResultsFromWorkerThreads(matches, accountId)
  return lolGamesStats.calculateMergedStatsResults(results)
 