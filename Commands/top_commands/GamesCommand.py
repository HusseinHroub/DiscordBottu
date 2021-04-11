from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor


class GamesCommand:
    def __init__(self, modeType=None):
        self.modeType = modeType

    def execute(self, commandArgs):
        return CommandResult([SimpleSortedListExtractor(ModeTypes.top, 'total_games').extract()])


def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lgames', 'Get top players based on games count')]
