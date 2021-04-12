from Commands.top_commands import SortedListCommand
from Commands.utils.command_usage import CommandUsage
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes


class TopHelpCommand:
    def getHelpUsage(self) -> [CommandUsage]:
        return SortedListCommand.getUsage(ModeTypes.top)
