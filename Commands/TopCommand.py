from TopExtractors.SimpleTopListExtractor import SimpleTopListExtractor
class TopCommand:
  def __init__(self, commandArgs):
    self.commandArgs = commandArgs
 
  def execute(self):
    stats = 'kills' if len(self.commandArgs) == 0 else self.commandArgs[0]
    return self.getTopListExtractor(stats).extract()    
 
  def getHelpMessage(self):
    return '\nHere is an example on how to use this command\n!ltop [this will get top list based on kills count] \n\n**You also can use one of the followings as valid commands:\n1- !ltop kills [this will get the top list based on kills count]\n2- !ltop deaths [this will get the top list baed on minimum deaths count]\n3- !ltop assists [this will get the top list based on assists count]\n4- ltop total [This will merge kills and deaths and assists, and return the global top list]'
  
  def getTopListExtractor(self, stats):
    topListExtractors = {
      'kills': SimpleTopListExtractor('kills'),
      'deaths': SimpleTopListExtractor('deaths'),
      'assists': SimpleTopListExtractor('assists'),
      'total': SimpleTopListExtractor('total')
    }
    
    topListExtractorObject = topListExtractors.get(stats, None)
    if(topListExtractorObject == None):
      raise Exception(f"Incorrect first argument, invalid stat value: {stats}" + self.getHelpMessage())
    return topListExtractorObject