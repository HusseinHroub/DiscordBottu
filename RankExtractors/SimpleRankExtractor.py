import dbutils


class SimpleRankExtractor:
    def __init__(self, statType):
        self.statType = statType

    def extract(self, summonerName, session):
        summoners_data = dbutils.getSummonersSortedByStat(self.statType, self.statType != 'deaths', session)
        counter = 0
        for summoner_data in summoners_data:
            counter = counter + 1
            if summoner_data.name.lower() == summonerName:
                return f"{summoner_data.name} {self.statType} rank is {counter} of {len(summoners_data)}, total {self.statType}: {summoner_data.__dict__[self.statType]}"
        return 'Sorry, wasnt able to locate summoner name'
