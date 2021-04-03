from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor, ModeTypes

defaultStat = 'avg_kda'


class SortedListCommand:
    def __init__(self, modeType, commandArgs):
        self.modeType = modeType
        self.commandArgs = commandArgs

    def execute(self):
        stats = defaultStat if len(self.commandArgs) == 0 else self.commandArgs[0]
        return self.getTopListExtractor(stats).extract()

    def getTopListExtractor(self, stats):
        modeType = ModeTypes.top if self.modeType == '!ltop' else ModeTypes.worst
        if stats == 'kills' or stats == 'kill':
            return SimpleSortedListExtractor(modeType, 'kills')
        elif stats == 'deaths' or stats == 'death':
            return SimpleSortedListExtractor(modeType, 'deaths')
        elif stats == 'assists' or stats == 'assist':
            return SimpleSortedListExtractor(modeType, 'assists')
        elif stats == 'avg_kda' or stats == 'kda':
            return SimpleSortedListExtractor(modeType, 'avg_kda')
        elif stats == 'farms' or stats == 'farm':
            return SimpleSortedListExtractor(modeType, 'farms')
        elif stats == 'total_games' or stats == 'games' or stats == 'games_count':
            return SimpleSortedListExtractor(modeType, 'total_games')
        else:
            raise ValueError(f"{self.modeType} {stats} is not a valid command, type !lhelp to get full list of available commands")
