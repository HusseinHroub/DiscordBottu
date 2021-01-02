from Commands.RegisterCommand import RegisterCommand
from Commands.RankCommand import RankCommand

def getCommand(command, commandArgs):
  commandObject = getCommandObject(command, commandArgs)
  if commandObject != None:
    return commandObject
  else:
    raise Exception(f"Command {command} doesn't exist")




def getCommandObject(command, commandArgs): 
    switcher = { 
        '!lregister': RegisterCommand(commandArgs), 
        '!lrank': RankCommand(commandArgs), 
    }   
    return switcher.get(command, None) 