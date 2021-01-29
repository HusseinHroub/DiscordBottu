from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor, ModeTypes

defaultStat = 'avg_kda'


class SortedListCommand:
    def __init__(self, modeType, commandArgs):
        self.modeType = modeType
        self.commandArgs = commandArgs

    def execute(self):
        stats = defaultStat if len(self.commandArgs) == 0 else self.commandArgs[0]
        return self.getTopListExtractor(stats).extract()

    def getHelpMessage(self):
        sortType = self.getType()

        return f'\nHere is an example on how to use this command\n{self.modeType} [this will get {sortType} list based on {defaultStat} count] \n\n**You also can use one of the followings as valid commands:\n1- {self.modeType} kills [this will get the {sortType} list based on kills count]\n2- {self.modeType} deaths [this will get the {sortType} list baed on {"minimum" if sortType == "top" else "maximum"} deaths count]\n3- {self.modeType} assists [this will get the {sortType} list based on assists count]\n4- {self.modeType} kda [this will get the kda {sortType} list]'

    def getType(self):
        return 'top' if self.modeType == '!ltop' else 'worst'

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
            raise Exception(f"Incorrect first argument, invalid stat value: {stats}" + self.getHelpMessage())
