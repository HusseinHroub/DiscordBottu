import enum
import sotrageutils


class ModeTypes(enum.Enum):
    top = 0
    worst = 1


class SimpleSortedListExtractor:
    def __init__(self, modeType, statType):
        self.modeType = modeType
        self.statType = statType

    def extract(self):
        summoners_data = sotrageutils.getSummonersSortedByStat(self.statType)
        response = ''
        counter = 1
        if self.isDesc():
            for summoner_data in summoners_data:
                response = response + self.getFormattedResponse(counter, summoner_data)
                counter = counter + 1
        else:
            for i in range(len(summoners_data), 0, -1):
                summoner_data = summoners_data[i - 1]
                response = response + self.getFormattedResponse(counter, summoner_data)
                counter = counter + 1
        return response

    def getFormattedResponse(self, counter, summoner_data):
        value = summoner_data[1]
        if self.statType == 'avg_kda':
            value = round(value, 2)
        return f'{counter}- {summoner_data[0]} with {value} {self.statType}\n\n'

    def isDesc(self):
        if self.modeType == ModeTypes.top:
            return self.statType != 'deaths'
        else:
            return self.statType == 'deaths'
