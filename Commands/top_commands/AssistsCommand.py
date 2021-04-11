from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor


class AssistsCommand:
    def __init__(self, modeType=None):
        self.modeType = modeType

    def execute(self, commandArgs):
        return CommandResult([SimpleSortedListExtractor(ModeTypes.top, 'assists').extract()])


def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lassists', 'Get top players based on assists count')]
