from Jobs.Tasks import lolStatUpdatorTask
class TempCommand:
  def __init__(self, commandArgs):
    self.commandArgs = commandArgs
 
  def execute(self):
    lolStatUpdatorTask.updateDBStats()