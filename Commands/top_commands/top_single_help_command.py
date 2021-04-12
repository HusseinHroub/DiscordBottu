from Commands.top_commands import KillsCommand, GamesCommand, AssistsCommand, DeathsCommand, FarmsCommand, KDACommand, \
    WinsRateCommand
from Commands.utils.command_usage import CommandUsage


class TopSingleHelpCommand:
    def getHelpUsage(self) -> [CommandUsage]:
        return KillsCommand.getUsage() + \
               DeathsCommand.getUsage() + \
               AssistsCommand.getUsage() + \
               FarmsCommand.getUsage() + \
               GamesCommand.getUsage() + \
               KDACommand.getUsage() + \
               WinsRateCommand.getUsage()
