from Commands.HelpCommand import HelpCommand
from Commands.base_commands.RankCommand import RankCommand
from Commands.base_commands.RegisterCommand import RegisterCommand
from Commands.dummy_commands.LeaveCommand import LeaveCommand
from Commands.top_commands.AssistsCommand import AssistsCommand
from Commands.top_commands.DeathsCommand import DeathsCommand
from Commands.top_commands.FarmsCommand import FarmsCommand
from Commands.top_commands.GamesCommand import GamesCommand
from Commands.top_commands.KDACommand import KDACommand
from Commands.top_commands.KillsCommand import KillsCommand
from Commands.top_commands.SortedListCommand import SortedListCommand
from Commands.top_commands.WinsRateCommand import WinsRateCommand
from SortedListExtractors.SimpleSortedListExtractor import ModeTypes

commands = {}


def getCommand(command):
    command = command.lower()
    commandObject = commands.get(command, None)
    if commandObject != None:
        return commandObject
    else:
        raise Exception(f"Command {command} doesn't exist, {getHelpMessage()}")


def getHelpMessage():
    return 'type !lhelp to see list of available commands'


def initCommands():
    global commands
    kill_command = KillsCommand()
    deaths_command = DeathsCommand()
    assists_command = AssistsCommand()
    farms_command = FarmsCommand()
    kda_command = KDACommand()
    games_command = GamesCommand()
    wins_rate_command = WinsRateCommand()
    commands = {
        '!lregister': RegisterCommand(),
        '!lrank': RankCommand(),
        '!ltop': SortedListCommand(ModeTypes.top),
        '!lworst': SortedListCommand(ModeTypes.worst),
        '!lkills': kill_command,
        '!lkill': kill_command,
        '!ldeath': deaths_command,
        '!ldeaths': deaths_command,
        '!lassists': assists_command,
        '!lassist': assists_command,
        '!lkda': kda_command,
        '!lavg_kda': kda_command,
        '!lavgkda': kda_command,
        '!lfarms': farms_command,
        '!lfarm': farms_command,
        '!lgames': games_command,
        '!ltotal_games': games_command,
        '!lgames_count': games_command,
        '!lgamescount': games_command,
        '!lwinrate': wins_rate_command,
        '!lwinsrate': wins_rate_command,
        '!leave': LeaveCommand(),
        '!lhelp': HelpCommand()

    }


initCommands()
