import dbutils


class SimpleRankExtractor:
    def __init__(self, statType):
        self.statType = statType

    def extract(self, summonerName, session):
        summoners_data = dbutils.getSummonersSortedByStat(self.statType, self.statType != 'deaths', session)
        rank, summoner_data = self.getSummonerRankDetails(summoners_data, summonerName)
        if rank != None:
            return f"{summoner_data.name} {self.statType} rank is {rank} of {len(summoners_data)}, total {self.statType}: {summoner_data.__getattribute__(self.statType)}"
        else:
            raise LookupError('Sorry, was not able to know the rank of this summoner :(')

    def getSummonerRankDetails(self, summoner_data_array, summonerName):
        counter = 0
        for summoner_data in summoner_data_array:
            counter = counter + 1
            if summoner_data.name.lower() == summonerName:
                return counter, summoner_data
        return None, None
