from lolutils import lolApiUtils
import dbutils
import time
import sotrageutils
from threading import Thread

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
    if(dbutils.isAccountIdExist(accountId)):
      dbutils.updateSummonerByAccountId(accountId = accountId, summonerName = summonerName)
      return f'Summoner is already registerred with old name, updated to the new provided name: {summonerName}'
    dbutils.insertSummoner(accountId, summonerName, *self.getStatsAndLastGameTimeStamp(accountId))
    self.updateCacheInAnotherThread()
    return f'Successfully registered {summonerName} in bot database'
  
  def getStatsAndLastGameTimeStamp(self, accountId):
    matches = lolApiUtils.getMatchesByAccountId(accountId)
    kills = 0
    deaths = 0
    assists = 0
    lastGameTimeStamp = time.time()
    if matches != None:
      lastGameTimeStamp = matches[0]['timestamp'] + 1
      kills, deaths, assists = lolApiUtils.getTotalStatsOfMatches(matches, accountId)
    return kills, deaths, assists, lastGameTimeStamp
  
  def updateCacheInAnotherThread(self):
     thread = Thread(target=sotrageutils.updateCache)
     thread.start()


