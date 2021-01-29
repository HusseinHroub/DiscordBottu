from lolutils import lolApiUtils
import dbutils
import time
import sotrageutils
from threading import Thread
from statsUtils import lolStatsMerger


class RegisterCommand:
    def __init__(self, commandArgs):
        self.commandArgs = commandArgs

    def execute(self):
        if len(self.commandArgs) == 0:
            return f"Error: summoner name wasn't provided, here is an example on how to use this command\n!lregister \"3amo Draven\""
        summonerName = self.commandArgs[0]
        if dbutils.isSummonerExist(summonerName.lower()):
            return f"Already have registerred summoner with name {summonerName}"
        accountId = lolApiUtils.getAccountIdByName(summonerName)
        if (dbutils.isAccountIdExist(accountId)):
            dbutils.updateSummonerByAccountId(accountId=accountId, summonerName=summonerName)
            return f'Summoner is already registerred with old name, updated to the new provided name: {summonerName}'
        lastGamesStats = self.getStatsAndLastGameTimeStamp(accountId)
        dbutils.insertSummoner(accountId, summonerName, lastGamesStats['total_kills'], lastGamesStats['total_deaths'],
                               lastGamesStats['total_assists'], lastGamesStats['lastGameTimeStamp'],
                               lastGamesStats['total_farms'], lastGamesStats['avg_kda'], lastGamesStats['sample_count'])
        self.updateCacheInAnotherThread()
        return f'Successfully registered {summonerName} in bot database'

    def getStatsAndLastGameTimeStamp(self, accountId):
        matches = lolApiUtils.getMatchesByAccountId(accountId)
        result = {'total_kills': 0, 'total_assists': 0, 'total_assists': 0, 'lastGameTimeStamp': time.time(),
                  'total_farms': 0, 'avg_kda': 0, 'numberOfGames': 0}
        if matches != None:
            matches_stats = lolApiUtils.getMatchesStats(matches, accountId)
            matches_merged_stat = lolStatsMerger.mergeGamesStats(matches_stats)
            result = {
                **matches_merged_stat, 'lastGameTimeStamp': matches[0]['timestamp'] + 1
            }
        return result

    def updateCacheInAnotherThread(self):
        thread = Thread(target=sotrageutils.updateCache)
        thread.start()
