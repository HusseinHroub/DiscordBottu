from Commands.RegisterCommand import RegisterCommand
from Commands.RankCommand import RankCommand
from Commands.TopCommand import TopCommand
from Commands.TempCommand import TempCommand

def getCommand(command, commandArgs):
  commandObject = getCommandObject(command, commandArgs)
  if commandObject != None:
    return commandObject
  else:
    raise Exception(f"Command {command} doesn't exist, {getHelpMessage()}")

def getCommandObject(command, commandArgs): 
    switcher = { 
        '!lregister': RegisterCommand(commandArgs), 
        '!lrank': RankCommand(commandArgs), 
        '!ltop': TopCommand(commandArgs),
        '!lhasonspec': TempCommand(commandArgs)
    }   
    return switcher.get(command, None) 

def getHelpMessage():
  return 'avaiable commands to use:\n!lrank "Summoner Name" [kills, deaths, assists, total]\n!ltop [kills, deaths, assists, total]\n!lregister "Summoner Name"'