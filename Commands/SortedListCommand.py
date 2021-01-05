from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor, ModeTypes
class SortedListCommand:
  def __init__(self, modeType, commandArgs):
    self.modeType = modeType
    self.commandArgs = commandArgs
 
  def execute(self):
    stats = 'kills' if len(self.commandArgs) == 0 else self.commandArgs[0]
    return self.getTopListExtractor(stats).extract()    
 
  def getHelpMessage(self):
    return f'\nHere is an example on how to use this command\n{self.modeType} [this will get top list based on kills count] \n\n**You also can use one of the followings as valid commands:\n1- {self.modeType} kills [this will get the top list based on kills count]\n2- {self.modeType} deaths [this will get the top list baed on minimum deaths count]\n3- {self.modeType} assists [this will get the top list based on assists count]\n4- {self.modeType} total [This will merge kills and deaths and assists, and return the global top list]'
  
  def getTopListExtractor(self, stats):
    modeType = ModeTypes.top if self.modeType == '!ltop' else ModeTypes.worst
    topListExtractors = {
      'kills': SimpleSortedListExtractor(modeType, 'kills'),
      'deaths': SimpleSortedListExtractor(modeType, 'deaths'),
      'assists': SimpleSortedListExtractor(modeType, 'assists'),
      'total': SimpleSortedListExtractor(modeType, 'total')
    }
    
    topListExtractorObject = topListExtractors.get(stats, None)
    if(topListExtractorObject == None):
      raise Exception(f"Incorrect first argument, invalid stat value: {stats}" + self.getHelpMessage())
    return topListExtractorObject