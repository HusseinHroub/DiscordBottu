from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor


class KDACommand:
    def __init__(self, modeType=None):
        self.modeType = modeType

    def execute(self, commandArgs):
        return CommandResult([SimpleSortedListExtractor(ModeTypes.top, 'avg_kda').extract()])


def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lkda', 'Get top players based on average kda count')]
