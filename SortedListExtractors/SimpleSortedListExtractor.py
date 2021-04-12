import enum
import os

import sotrageutils
from SortedListExtractors.formatters.SimpleRankViewFormatter import SimpleRankViewFormatter
from geric_view_formatters.tabular_string_formatter import TabularStringFormatter


class ModeTypes(enum.Enum):
    top = 0
    worst = 1

RANKS_DATA_FORMAT = os.getenv('RANKS_DATA_FORMAT')

class SimpleSortedListExtractor:
    def __init__(self, modeType, statType):
        self.modeType = modeType
        self.statType = statType

    def extract(self):
        summoners_data = sotrageutils.getSummonersSortedByStat(self.statType)
        ranks_data = self.get_ranks_data(summoners_data)
        return self.get_ranks_data_fromatter().format(ranks_data)

    def get_ranks_data(self, summoners_data):
        counter = 1
        ranks_data = [['Rank', 'Summoner', self.statType]]
        if self.isDesc():
            for summoner_data in summoners_data:
                ranks_data.append(self.get_rank_row(counter, summoner_data))
                counter = counter + 1
        else:
            for i in range(len(summoners_data), 0, -1):
                summoner_data = summoners_data[i - 1]
                ranks_data.append(self.get_rank_row(counter, summoner_data))
                counter = counter + 1
        return ranks_data

    def isDesc(self):
        if self.modeType == ModeTypes.top:
            return self.statType != 'deaths'
        else:
            return self.statType == 'deaths'

    def get_rank_row(self, counter, summoner_data):
        summoner_name = summoner_data[0]
        value = summoner_data[1]
        if self.statType == 'avg_kda':
            value = round(summoner_data[1], 2)
        return [counter, summoner_name, value]

    def get_ranks_data_fromatter(self):
        if RANKS_DATA_FORMAT == 'table':
            return TabularStringFormatter()
        else:
            return SimpleRankViewFormatter()
