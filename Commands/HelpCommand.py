from Commands.base_commands.base_help_command import BaseCommandsHelp
from Commands.dummy_commands.NewLineCommandHelpUsage import NewLineCommandHelpUsage
from Commands.top_commands.top_help_command import TopHelpCommand
from Commands.top_commands.top_single_help_command import TopSingleHelpCommand
from Commands.top_commands.worst_help_command import WorstHelpCommand
from Commands.utils.command_result import CommandResult
from geric_view_formatters.tabular_string_formatter import TabularStringFormatter


class HelpCommand:
    def execute(self, commandArgs):
        commandsUsages = self.getCommandsUsageData([BaseCommandsHelp(),
                                                    NewLineCommandHelpUsage(),
                                                    TopSingleHelpCommand(),
                                                    NewLineCommandHelpUsage(),
                                                    TopHelpCommand(),
                                                    WorstHelpCommand()])
        return CommandResult([TabularStringFormatter().format(commandsUsages, tablefmt='simple')], embed_result=False)

    def getCommandUsageData(self, commandHelp):
        commandHelpUsageData = [['Command', 'Description']]
        for commandUsage in commandHelp.getHelpUsage():
            commandHelpUsageData.append([commandUsage.commandString, commandUsage.commandDesc])
        return commandHelpUsageData

    def getCommandsUsageData(self, commands):
        commandHelpUsageData = [['Command', 'Description']]
        for command in commands:
            for commandUsage in command.getHelpUsage():
                commandHelpUsageData.append([commandUsage.commandString, commandUsage.commandDesc])
        return commandHelpUsageData
