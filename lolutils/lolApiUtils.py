import requests
import os
from ratelimit import limits, sleep_and_retry
from lolutils import lolGamesStats
import time

region = 'euw1'
api_key = os.getenv('LAPIKEY')
root_url = f'https://{region}.api.riotgames.com/lol'

CALLS_NUMBER = 80
CALLS_PERIOD = 120
RETRYING_ATTEMPS = 3

@sleep_and_retry
@limits(calls=CALLS_NUMBER, period=CALLS_PERIOD)
def getJsonResponseOfUrl(url):
  return doGetJsonResponseOfUrl(url)

@sleep_and_retry
@limits(calls=15, period=2)
def doGetJsonResponseOfUrl(url, retryingAttemps = RETRYING_ATTEMPS):
  response = requests.get(url)
  status_code = response.status_code
  if status_code == 200:
    return response.json()
  if status_code == 404:
    return None
  
  print(f'got {status_code} status Code, retrying attemps = {retryingAttemps}')
  if retryingAttemps < 1:
     raise Exception(f'Tried to retry the request to avoid {status_code} but failed')
  print(f'sleeping for {RETRYING_ATTEMPS - retryingAttemps + 1} seconds then will retry')
  time.sleep(RETRYING_ATTEMPS - retryingAttemps + 1)
  return doGetJsonResponseOfUrl(url, retryingAttemps - 1)

  
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
    particpantDetails = match_details['participants'][particpantId - 1]
    stats = particpantDetails['stats'] 
    stats['championId'] = particpantDetails['championId']
    stats['queueId'] = match_details['queueId']
    return stats    
  else:
    raise Exception(f'Error cloudnt find particpantId of gameId: {gameId}')

def getMatchesStats(matches, accountId):
 return lolGamesStats.getStatResultsFromWorkerThreads(matches, accountId)
 