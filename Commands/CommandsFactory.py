from Commands.RegisterCommand import RegisterCommand
def getCommand(command, commandArgs):
  if(command == '!lrank'):
    return RegisterCommand(commandArgs)
  else:
    raise Exception(f"Command {command} doesn't exist")
