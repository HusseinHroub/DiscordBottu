from db_low_level import SummonerData, CommonTable


class SummonerDataModel:
    def __init__(self, accountId=None, name=None, kills=None, deaths=None, assists=None, lastGameTimeStamp=None,
                 avg_kda=None, farms=None, total_games=None):
        self.accountId = accountId
        self.name = name
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.lastGameTimeStamp = lastGameTimeStamp
        self.avg_kda = avg_kda
        self.farms = farms
        self.total_games = total_games

    def buildWithDataObject(self, dataObject: SummonerData):
        self.accountId = dataObject.__dict__['accountId']
        self.name = dataObject.name
        self.kills = dataObject.kills
        self.deaths = dataObject.deaths
        self.assists = dataObject.assists
        self.lastGameTimeStamp = dataObject.lastGameTimeStamp
        self.avg_kda = dataObject.avg_kda
        self.farms = dataObject.farms
        self.total_games = dataObject.total_games


class CommonTableModel:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def buildWithDataObject(self, dataObject: CommonTable):
        self.key = dataObject.key
        self.value = dataObject.value
