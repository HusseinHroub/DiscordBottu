import os

from ratelimit import limits, sleep_and_retry

from lolutils import lolGamesStats
from lolutils.constants import QUEUE_ID_GAME_TYPE_MAPPING
from requestUtls import utils

region = 'euw1'
region_v5 = 'europe'
api_key = os.getenv('LAPIKEY')
root_url = f'https://{region}.api.riotgames.com/lol'
root_url_v5 = f'https://{region_v5}.api.riotgames.com/lol'
CALLS_NUMBER = 40
CALLS_PERIOD = 120


@sleep_and_retry
@limits(calls=CALLS_NUMBER, period=CALLS_PERIOD)
def getJsonResponseOfUrl(url):
    return doGetJsonResponseOfUrl(url)


@sleep_and_retry
@limits(calls=15, period=2)
def doGetJsonResponseOfUrl(url):
    return utils.getHTTPJsonResponse(url)


def getAccountIdByName(name):
    jsonResponse = getJsonResponseOfUrl(f'{root_url}/summoner/v4/summoners/by-name/{name}?api_key={api_key}')
    if jsonResponse == None:
        raise Exception(f"Couldn't find summoner with name: {name}")
    return jsonResponse['puuid']


def get_target_queues():
    keys = ''
    for key in QUEUE_ID_GAME_TYPE_MAPPING.keys():
        keys += f'queue={key}&'
    return keys


def getMatchesByAccountId(accountId, beginTime=0):
    jsonResponse = getJsonResponseOfUrl(
        f'{root_url_v5}/match/v5/matches/by-puuid/{accountId}/ids?api_key={api_key}&count=100&startTime={beginTime}')
    return jsonResponse


def getParticipantObjectOfMatchDetails(match_details, accountId):
    participantIdentities = match_details['info']['participants']
    for participantIdentity in participantIdentities:
        if participantIdentity['puuid'] == accountId:
            return participantIdentity
    return None


def getStatsOfGameId(gameId, accountId):
    match_details = getJsonResponseOfUrl(f'{root_url_v5}/match/v5/matches/{gameId}?api_key={api_key}')
    particpantDetails = getParticipantObjectOfMatchDetails(match_details, accountId)
    if particpantDetails is not None:
        particpantDetails['queueId'] = match_details['info']['queueId']
        particpantDetails['gameEndTimestamp'] = match_details['info']['gameEndTimestamp']
        return particpantDetails
    else:
        raise Exception(f'Error cloudnt find particpantId of gameId: {gameId}')


def getMatchesStats(matches, accountId):
    return lolGamesStats.getTotalStatsOfMatches(matches, accountId)
