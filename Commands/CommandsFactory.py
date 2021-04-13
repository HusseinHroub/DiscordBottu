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


def getCommand(command):
    command = command.lower()
    commandObject = getCommandOrNone(command)
    if commandObject != None:
        return commandObject
    else:
        raise ValueError(f"Command {command} doesn't exist, {getHelpMessage()}")


def getHelpMessage():
    return 'type !lhelp to see list of available commands'


def getCommandOrNone(command):
    if command == '!lregister':
        return RegisterCommand()
    if command == '!lrank':
        return RankCommand()
    if command == '!ltop':
        return SortedListCommand(ModeTypes.top)
    if command == '!lworst':
        return SortedListCommand(ModeTypes.worst)
    if command == '!lkills' or command == '!lkill':
        return KillsCommand()
    if command == '!ldeath' or command == '!ldeaths':
        return DeathsCommand()
    if command == '!lassist' or command == '!lassists':
        return AssistsCommand()
    if command == '!lkda' or command == '!lavg_kda' or command == '!lavgkda':
        return KDACommand()
    if command == '!lfarm' or command == '!lfarms':
        return FarmsCommand()
    if command == '!lgames' or command == '!ltotal_games' or command == '!lgames_count' or command == '!lgamescount':
        return GamesCommand()
    if command == '!lwinrate' or command == '!lwinsrate':
        return WinsRateCommand()
    if command == '!leave':
        return LeaveCommand()
    if command == '!lhelp':
        return HelpCommand()
