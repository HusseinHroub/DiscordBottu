from Commands.RegisterCommand import RegisterCommand
from Commands.RankCommand import RankCommand
from Commands.SortedListCommand import SortedListCommand
from Commands.LeaveCommand import LeaveCommand


def getCommand(command, commandArgs):
    command = command.lower()
    commandObject = getCommandObject(command, commandArgs)
    if commandObject != None:
        return commandObject
    else:
        raise Exception(f"Command {command} doesn't exist, {getHelpMessage()}")


def getCommandObject(command, commandArgs):
    lowerCommandVersionArgs = [str.lower() for str in commandArgs]
    switcher = {
        '!lregister': RegisterCommand(commandArgs),
        '!lrank': RankCommand(lowerCommandVersionArgs),
        '!ltop': SortedListCommand(command, lowerCommandVersionArgs),
        '!lworst': SortedListCommand(command, lowerCommandVersionArgs),
        '!leave': LeaveCommand()

    }
    return switcher.get(command, None)


def getHelpMessage():
    return 'avaiable commands to use:\n!lrank "Summoner Name" [kills, deaths, assists, kda]\n!ltop or !lworst [kills, deaths, assists, kda, farms, games]\n!lregister "Summoner Name"'
