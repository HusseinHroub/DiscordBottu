from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor


class FarmsCommand:
    def __init__(self, modeType=None):
        self.modeType = modeType

    def execute(self, commandArgs):
        return CommandResult([SimpleSortedListExtractor(ModeTypes.top, 'farms').extract()])


def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lfarms', 'Get top players based on farms count')]
