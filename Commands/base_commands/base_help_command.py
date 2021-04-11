from Commands.base_commands import RankCommand, RegisterCommand
from Commands.utils.command_usage import CommandUsage


class BaseCommandsHelp:
    def getHelpUsage(self) -> [CommandUsage]:
        return RegisterCommand.getUsage() + RankCommand.getUsage()