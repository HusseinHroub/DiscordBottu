from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor

defaultStat = 'avg_kda'


class SortedListCommand:
    def __init__(self, modeType):
        self.modeType = modeType

    def execute(self, commandArgs):
        commandArgs = [str.lower() for str in commandArgs]
        stats = defaultStat if len(commandArgs) == 0 else commandArgs[0]
        return CommandResult([self.getTopListExtractor(stats).extract()])

    def getTopListExtractor(self, stats):
        if stats == 'kills' or stats == 'kill':
            return SimpleSortedListExtractor(self.modeType, 'kills')
        elif stats == 'deaths' or stats == 'death':
            return SimpleSortedListExtractor(self.modeType, 'deaths')
        elif stats == 'assists' or stats == 'assist':
            return SimpleSortedListExtractor(self.modeType, 'assists')
        elif stats == 'avg_kda' or stats == 'kda':
            return SimpleSortedListExtractor(self.modeType, 'avg_kda')
        elif stats == 'farms' or stats == 'farm':
            return SimpleSortedListExtractor(self.modeType, 'farms')
        elif stats == 'total_games' or stats == 'games' or stats == 'games_count':
            return SimpleSortedListExtractor(self.modeType, 'total_games')
        elif stats == 'winrate' or stats == 'winsrate':
            return SimpleSortedListExtractor(self.modeType, 'win_rate')
        else:
            raise ValueError(
                f"{stats} is not valid stat, type !lhelp to get full list of available commands")


def getUsage(modeType) -> [CommandUsage]:
    if modeType == ModeTypes.top:
        return [
            CommandUsage('!ltop [kills|deaths|assists|farms|games|wins_rate|kda]',
                         'Get top players based on given stat'), ]
    else:
        return [CommandUsage('!lworst [kills|deaths|assists|farms|games|wins_rate|kda]',
                             'Get worst players based on given stat')]
