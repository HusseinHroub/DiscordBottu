import requests
import os
from ratelimit import limits, sleep_and_retry
region = 'euw1'
api_key = os.getenv('LAPIKEY')
root_url = f'https://{region}.api.riotgames.com/lol'

CALLS_NUMBER = 50
CALLS_PERIOD = 60

@sleep_and_retry
@limits(calls=CALLS_NUMBER, period=CALLS_PERIOD)
def getJsonResponseOfUrl(url):
  response = requests.get(url)
  if response.status_code != 200:
    raise Exception(f'While trying to get url request, got the following response code: {response.status_code}')
  return response.json()

def getAccountIdByName(name):
  return getJsonResponseOfUrl(f'{root_url}/summoner/v4/summoners/by-name/{name}?api_key={api_key}')['accountId']


def getMatchesByAccountId(accountId):
  return getJsonResponseOfUrl(f'{root_url}/match/v4/matchlists/by-account/{accountId}?api_key={api_key}')['matches']
  
    

def getParticpantIdOfGameDetails(match_details, accountId):
  participantIdentities = match_details['participantIdentities']
  for participantIdentity in participantIdentities:
    if participantIdentity['player']['accountId'] == accountId:
      return participantIdentity['participantId']
  return -1


def getKillsOfGameId(gameId, accountId):
  match_details = getJsonResponseOfUrl(f'{root_url}/match/v4/matches/{gameId}?api_key={api_key}')
  particpantId = getParticpantIdOfGameDetails(match_details, accountId)
  if particpantId != -1:
    return match_details['participants'][particpantId - 1]['stats']['kills']
  else:
    print(f'warning cloudnt find particpantId of gameId: {gameId}')
    return 0

def getTotalKillsOfMatches(matches, accountId):
  total_kills = 0
  for match in matches:
    total_kills += getKillsOfGameId(match["gameId"], accountId)
  return total_kills