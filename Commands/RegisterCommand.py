import time
from threading import Thread

import dbutils
import sotrageutils
from lolutils import lolApiUtils


class RegisterCommand:
    def __init__(self, commandArgs):
        self.commandArgs = commandArgs

    @dbutils.SessionManager
    def execute(self, session):
        if len(self.commandArgs) == 0:
            return f"Error: summoner name wasn't provided, here is an example on how to use this command\n!lregister \"3amo Draven\""
        summonerName = self.commandArgs[0]
        if dbutils.isSummonerNameExist(summonerName.lower(), session):
            return f"Already have registered summoner with name {summonerName}"
        accountId = lolApiUtils.getAccountIdByName(summonerName)
        if (dbutils.isAccountIdExist(accountId, session)):
            dbutils.updateSummonerNameByAccountId(accountId, summonerName, session)
            return f'Summoner is already registered with old name, updated to the new provided name: {summonerName}'
        dbutils.insertSummoner(accountId, summonerName, self.getCurrentEpochTime(), session)
        self.updateCacheInAnotherThread()
        return f'Successfully registered {summonerName} in bot database'

    def updateCacheInAnotherThread(self):
        thread = Thread(target=sotrageutils.updateStatCache)
        thread.start()

    def getCurrentEpochTime(self):
        return int(time.time() * 1000)
