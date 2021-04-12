import dbutils
from Commands.utils.command_result import CommandResult
from Commands.utils.command_usage import CommandUsage
from RankExtractors.SimpleRankExtractor import SimpleRankExtractor

defaultStat = 'avg_kda'


class RankCommand:

    @dbutils.SessionManager
    def execute(self, commandArgs, session):
        commandArgs = [str.lower() for str in commandArgs]
        if len(commandArgs) == 0:
            raise ValueError(
                'Summoner name wasn\'t provided, provide summoner name with !lrank\nExample: !lrank "3amo batte5"')
        summonerName = commandArgs[0]
        stats = defaultStat if len(commandArgs) == 1 else commandArgs[1]
        rankExtractor = self.getRankExtractor(stats)
        if not dbutils.isSummonerNameExist(summonerName, session):
            raise LookupError(
                f"It seems this summoner name {summonerName} is not registerred, please register this summoner first using this command\n!lregister \"{summonerName}\"")
        return CommandResult([rankExtractor.extract(summonerName, session)])

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
        if (rankExtractorObject == None):
            raise ValueError(
                f"!lrank {stats} is not a valid command, type !lhelp to get full list of available commands")
        return rankExtractorObject

def getUsage() -> [CommandUsage]:
    return [CommandUsage('!lrank "Summoner Name"', 'Get rank of a summoner by name')]
