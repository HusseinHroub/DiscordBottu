import time
from threading import Thread

import dbutils
import sotrageutils
from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from lolutils import lolApiUtils


class RegisterCommand:

    @dbutils.SessionManager
    def execute(self, commandArgs, session):
        if len(commandArgs) == 0:
            raise ValueError(
                f"Summoner name wasn't provided, here is an example on how to use this command\n!lregister \"3amo Draven\"")
        summonerName = commandArgs[0]
        if dbutils.isSummonerNameExist(summonerName.lower(), session):
            raise AttributeError(f"Already have registered summoner with name {summonerName}")
        accountId = lolApiUtils.getAccountIdByName(summonerName)
        if (dbutils.isAccountIdExist(accountId, session)):
            dbutils.updateSummonerNameByAccountId(accountId, summonerName, session)
            session.commit()
            self.updateCacheInAnotherThread()
            raise AttributeError(
                f'Summoner is already registered with old name, updated to the new provided name: {summonerName}')
        dbutils.insertSummoner(accountId, summonerName, self.getCurrentEpochTime() / 1000, session)
        self.updateCacheInAnotherThread()
        return CommandResult([f'Successfully registered {summonerName} in bot database'])

    def updateCacheInAnotherThread(self):
        thread = Thread(target=sotrageutils.updateStatCache)
        thread.start()

    def getCurrentEpochTime(self):
        return int(time.time() * 1000)


def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lregister "Summoner Name"', 'Register summoner into bot DB (only EUW)')]
