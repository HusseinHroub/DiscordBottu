import dbutils
from RankExtractors.SimpleRankExtractor import SimpleRankExtractor
defaultStat = 'avg_kda'
class RankCommand:
  def __init__(self, commandArgs):
    self.commandArgs = commandArgs
 
  def execute(self):
    if len(self.commandArgs) == 0:
      return "Error: summoner name wasn't provided," + self.getHelpMessage()
    summonerName = self.commandArgs[0]
    stats = defaultStat if len(self.commandArgs) == 1 else self.commandArgs[1]
    rankExtractor = self.getRankExtractor(stats)
    if not dbutils.isSummonerExist(summonerName):
      return f"It seems this summoner name {summonerName} is not registerred, please register this summoner first using this command\n!lregister \"{summonerName}\""
    return rankExtractor.extract(summonerName)
    

  def getHelpMessage(self):
    return '\nHere is an example on how to use this command\n!lrank \"3amo Draven\" [this will get the rank based on avg_kda count] \n\n**You also can use one of the followings as valid commands:\n1- !lrank \"3amo Draven\" kills [this will get the rank based on kills count]\n2- !lrank \"3amo Draven\" deaths [this will get the rank baed on deaths count]\n3- !lrank \"3amo Draven\" assists [this will get the rank based on assists count]\n4- !lrank \"3amo Draven\" avg_kda [This rank based on avg_kda]'
  
  def getRankExtractor(self, stats):
    rankExtractors = {
      'kills': SimpleRankExtractor('kills'),
      'deaths': SimpleRankExtractor('deaths'),
      'assists': SimpleRankExtractor('assists'),
      'avg_kda': SimpleRankExtractor('avg_kda'),
      'kda': SimpleRankExtractor('kda'),
      'farms': SimpleRankExtractor('farms'),
      'total_games': SimpleRankExtractor('total_games'),
    }
    
    rankExtractorObject = rankExtractors.get(stats, None)
    if(rankExtractorObject == None):
      raise Exception(f"Incorrect second argument, invalid stat value: {stats}" + self.getHelpMessage())
    return rankExtractorObject

