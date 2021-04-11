from Commands.top_commands import SortedListCommand
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes


class WorstHelpCommand:
    def getHelpUsage(self) -> [CommandUsage]:
        return SortedListCommand.getUsage(ModeTypes.worst)
