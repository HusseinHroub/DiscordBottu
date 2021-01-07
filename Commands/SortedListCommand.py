from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor, ModeTypes

defaultStat = 'kda'
class SortedListCommand:
  def __init__(self, modeType, commandArgs):
    self.modeType = modeType
    self.commandArgs = commandArgs
 
  def execute(self):
    stats = defaultStat if len(self.commandArgs) == 0 else self.commandArgs[0]
    return self.getTopListExtractor(stats).extract()    
 
  def getHelpMessage(self):
    sortType = self.getType()

    return f'\nHere is an example on how to use this command\n{self.modeType} [this will get {sortType} list based on kills count] \n\n**You also can use one of the followings as valid commands:\n1- {self.modeType} kills [this will get the {sortType} list based on kills count]\n2- {self.modeType} deaths [this will get the {sortType} list baed on {"minimum" if sortType == "top" else "maximum"} deaths count]\n3- {self.modeType} assists [this will get the {sortType} list based on assists count]\n4- {self.modeType} total [This will merge kills and deaths and assists, and return the global {sortType} list]'
  
  def getType(self):
    return 'top' if self.modeType == '!ltop' else 'worst'

  def getTopListExtractor(self, stats):
    modeType = ModeTypes.top if self.modeType == '!ltop' else ModeTypes.worst
    topListExtractors = {
      'kills': SimpleSortedListExtractor(modeType, 'kills'),
      'deaths': SimpleSortedListExtractor(modeType, 'deaths'),
      'assists': SimpleSortedListExtractor(modeType, 'assists'),
      'kda': SimpleSortedListExtractor(modeType, 'kda')
    }
    
    topListExtractorObject = topListExtractors.get(stats, None)
    if(topListExtractorObject == None):
      raise Exception(f"Incorrect first argument, invalid stat value: {stats}" + self.getHelpMessage())
    return topListExtractorObject