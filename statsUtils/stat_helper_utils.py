import cacheutils
import dbutils
import sotrageutils


class StatBase:
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        pass

    def isEligibleForAnnouncment(self, matchStat):
        return False

    def getAnnouncmentNameValue(self, matchStat):
        pass

    def addFieldToTopEmbed(self, embed):
        pass

    def getResettedNameValue(self):
        pass

    def updateCache(self, session):
        pass


class KillsHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'kills': result['total_kills'] + summonerDataModel.kills}

    def isEligibleForAnnouncment(self, matchStat):
        return matchStat['kills'] > 19

    def getAnnouncmentNameValue(self, matchStat):
        return {'name': 'Kills', 'value': matchStat["kills"]}

    def addFieldToTopEmbed(self, embed):
        topKillsSummoner = sotrageutils.getTopKillsList()[0]
        addTopEmbedFiled(embed, 'Kills', topKillsSummoner[0], topKillsSummoner[1])

    def getResettedNameValue(self):
        return {'kills': 0}

    def updateCache(self, session):
        cacheutils.topKills = dbutils.getSummonersSortedByStat('kills', True, session)


class DeathsHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'deaths': result['total_deaths'] + summonerDataModel.deaths}

    def isEligibleForAnnouncment(self, matchStat):
        return matchStat['deaths'] > 14

    def getAnnouncmentNameValue(self, matchStat):
        return {'name': 'Deaths (waaw!)', 'value': matchStat["deaths"]}

    def addFieldToTopEmbed(self, embed):
        topDeathsSummoner = sotrageutils.getTopDeathsList()[0]
        addTopEmbedFiled(embed, 'Deaths', topDeathsSummoner[0], topDeathsSummoner[1])

    def getResettedNameValue(self):
        return {'deaths': 0}

    def updateCache(self, session):
        cacheutils.topDeaths = dbutils.getSummonersSortedByStat('deaths', False, session)


class AssistsHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'assists': result['total_assists'] + summonerDataModel.assists}

    def isEligibleForAnnouncment(self, matchStat):
        return matchStat['assists'] > 19

    def getAnnouncmentNameValue(self, matchStat):
        return {'name': 'Assists', 'value': matchStat["assists"]}

    def addFieldToTopEmbed(self, embed):
        topAssistsSummoner = sotrageutils.getTopAssistsList()[0]
        addTopEmbedFiled(embed, 'Assists', topAssistsSummoner[0], topAssistsSummoner[1])

    def getResettedNameValue(self):
        return {'assists': 0}

    def updateCache(self, session):
        cacheutils.topAssists = dbutils.getSummonersSortedByStat('assists', True, session)


class FarmsHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'farms': result['total_farms'] + summonerDataModel.farms}

    def addFieldToTopEmbed(self, embed):
        topFarmsSummoner = sotrageutils.getTopFarmsList()[0]
        addTopEmbedFiled(embed, 'Farms', topFarmsSummoner[0], topFarmsSummoner[1])

    def getResettedNameValue(self):
        return {'farms': 0}

    def updateCache(self, session):
        cacheutils.topFarms = dbutils.getSummonersSortedByStat('farms', True, session)


class GamesHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'total_games': result['sample_count'] + summonerDataModel.total_games}

    def addFieldToTopEmbed(self, embed):
        topGamesSummoner = sotrageutils.getTopGamesList()[0]
        addTopEmbedFiled(embed, 'Games Count', topGamesSummoner[0], topGamesSummoner[1])

    def getResettedNameValue(self):
        return {'total_games': 0}

    def updateCache(self, session):
        cacheutils.topTotalGames = dbutils.getSummonersSortedByStat('total_games', True, session)


class KDAHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        newCount = result['sample_count']
        oldCount = summonerDataModel.total_games
        newKDA = result['avg_kda']
        oldKda = summonerDataModel.avg_kda
        totalCount = newCount + oldCount
        return {'avg_kda': newKDA if oldCount == 0 else (oldKda + (newKDA - oldKda) / totalCount)}

    def addFieldToTopEmbed(self, embed):
        topKDASummoner = sotrageutils.getTopKDAList()[0]
        addTopEmbedFiled(embed, 'Average KDA', topKDASummoner[0], topKDASummoner[1])

    def getResettedNameValue(self):
        return {'avg_kda': 0}

    def updateCache(self, session):
        cacheutils.topAvgKda = dbutils.getSummonersSortedByStat('avg_kda', True, session)


class WinsHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'wins': result['wins'] + summonerDataModel.wins}

    def getResettedNameValue(self):
        return {'wins': 0}

    def updateCache(self, session):
        cacheutils.topWinsRate = dbutils.getSummonersSortedByStat('win_rate', True, session)


class LosesHelper(StatBase):
    def mergeResultWithSummonerData(self, result, summonerDataModel):
        return {'loses': result['loses'] + summonerDataModel.loses}

    def getResettedNameValue(self):
        return {'loses': 0}


def addTopEmbedFiled(embed, category, summonerName, topValue):
    embed.add_field(name=f'Top {category}', value=f'{summonerName} with {topValue} {category.lower()}',
                    inline=False)


stat_helpers = [KillsHelper(),
                DeathsHelper(),
                AssistsHelper(),
                FarmsHelper(),
                GamesHelper(),
                KDAHelper(),
                WinsHelper(),
                LosesHelper()]
