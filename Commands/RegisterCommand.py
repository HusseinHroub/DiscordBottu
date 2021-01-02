import lolApiUtils
import dbutils

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
    dbutils.insertSummoner(accountId, summonerName)
    return f'Succefully registered {summonerName} in bot database'

