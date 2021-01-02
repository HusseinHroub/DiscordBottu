class RegisterCommand:
  def __init__(self, commandArgs):
    self.commandArgs = commandArgs

  def execute(self):
    return f'in register command, args are: {self.commandArgs}'

