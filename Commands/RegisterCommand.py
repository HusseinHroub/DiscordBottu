import lolApiUtils
import dbutils
import time

class RegisterCommand:
  def __init__(self, commandArgs):
    self.commandArgs = commandArgs

  def execute(self):
    if len(self.commandArgs) == 0:
      return f"Error: summoner name wasn't provided, here is an example on how to use this command\n!lregister \"3amo Draven\"" 
    summonerName = self.commandArgs[0]
    if dbutils.isSummonerExist(summonerName):
      return f"Already have registerred summoner with name {summonerName}"
    accountId = lolApiUtils.getAccountIdByName(summonerName)
    dbutils.insertSummoner(accountId, summonerName, *self.getStatsAndLastGameTimeStamp(accountId))
    return f'Succefully registered {summonerName} in bot database'
  
  def getStatsAndLastGameTimeStamp(self, accountId):
    matches = lolApiUtils.getMatchesByAccountId(accountId, 1609440853582)
    kills = 0
    deaths = 0
    assists = 0
    lastGameTimeStamp = time.time()
    if matches != None:
      lastGameTimeStamp = matches[0]['timestamp'] + 1
      kills, deaths, assists = lolApiUtils.getTotalStatsOfMatches(matches, accountId)
    return kills, deaths, assists, lastGameTimeStamp


