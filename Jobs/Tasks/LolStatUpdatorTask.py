import asyncio
import calendar
import traceback
from datetime import datetime
from queue import Queue
from threading import Thread

import discord

import dbutils
import sotrageutils
from lolutils import constants
from lolutils import lolApiUtils
from statsUtils import lolStatsMerger


class LolStatUpdatorTask:
    def __init__(self, channel, loop):
        self.channel = channel
        self.loop = loop

    @dbutils.SessionManager
    def execute(self, session):
        self.resetStatsIfStartOfMonth(session)
        self.startUpdateProcess(session)

    def resetStatsIfStartOfMonth(self, session):
        if datetime.today().day == 1:
            if sotrageutils.getMonthAnnouncedValue() == 'False':
                self.shareTopPlayersStatsPerCategory()
                dbutils.resetStats(session)
                sotrageutils.markMonthAnnouncedValue('True', session)
                sotrageutils.updateStatCache(session)
                session.commit()
        else:
            if sotrageutils.getMonthAnnouncedValue() == 'True':
                sotrageutils.markMonthAnnouncedValue('False', session)
                session.commit()

    def startUpdateProcess(self, session):
        summonersDatabaseResults = dbutils.getAllSummonerData(session)
        summonersLolAPIResults = self.getSummonersAPIStats(summonersDatabaseResults)
        summonersMergedResults = self.mergeSummonersDataBaseAndAPIResults(summonersDatabaseResults,
                                                                          summonersLolAPIResults)
        self.updateToDBIfNotEmptyData(summonersMergedResults, session)
        self.shareAnnouncmentMessagesInDB(summonersLolAPIResults, summonersDatabaseResults)

    def getSummonersAPIStats(self, summonersData):
        queue = Queue(maxsize=0)
        numberOfThreads = min(30, len(summonersData))
        results = [None for x in summonersData]
        for i in range(len(summonersData)):
            queue.put((i, summonersData[i]))
        threads = []
        for i in range(numberOfThreads):
            worker = Thread(target=self.getTotalStatsOfSummonerWorker, args=(queue, results))
            threads.append(worker)
            worker.start()
        for worker in threads:
            worker.join()
        return results

    def getTotalStatsOfSummonerWorker(self, queue, results):
        while not queue.empty():
            work = queue.get()
            summonerDataModel = work[1]
            matches = lolApiUtils.getMatchesByAccountId(summonerDataModel.accountId,
                                                        summonerDataModel.lastGameTimeStamp)
            if matches != None and len(matches) > 0:
                try:
                    matches_stats = lolApiUtils.getMatchesStats(matches, summonerDataModel.accountId)
                    matches_merged_stat = lolStatsMerger.mergeGamesStats(matches_stats)
                    result = {
                        **matches_merged_stat,
                        'lastGameTimeStamp': matches[0]['timestamp'] + 1,
                        'accountId': summonerDataModel.accountId
                    }
                    results[work[0]] = {'totalStatsResult': result, 'matchesStats': matches_stats}
                except:
                    print('error happened while updating player stats!')
                    traceback.print_exc()

    def mergeSummonersDataBaseAndAPIResults(self, summonersData, results):
        newSummonersData = []
        for i in range(len(summonersData)):
            if results[i] == None:
                continue
            result = results[i]['totalStatsResult']
            summonerDataModel = summonersData[i]
            newSummonersData.append({
                'kills': result['total_kills'] + summonerDataModel.kills,
                'deaths': result['total_deaths'] + summonerDataModel.deaths,
                'assists': result['total_assists'] + summonerDataModel.assists,
                'farms': result['total_farms'] + summonerDataModel.farms,
                'accountId': summonerDataModel.accountId,
                'lastGameTimeStamp': result['lastGameTimeStamp'],
                **self.getKDAInfo(result['avg_kda'], summonerDataModel.avg_kda, result['sample_count'],
                                  summonerDataModel.total_games)
            })
        return newSummonersData

    def getKDAInfo(self, newKDA, oldKda, newCount, oldCount):
        totalCount = newCount + oldCount
        return {
            'avg_kda': oldKda + (newKDA - oldKda) / totalCount,
            'total_games': totalCount
        }

    def updateToDBIfNotEmptyData(self, newSummonersData, session):
        if newSummonersData != None and len(newSummonersData) > 0:
            print('updating db!')
            session.bulk_update_mappings(dbutils.SummonerData, newSummonersData)
            sotrageutils.updateStatCache(session)

    def shareAnnouncmentMessagesInDB(self, results, summonersData):
        for i in range(len(results)):
            if results[i] == None:
                continue
            matchesStats = results[i]['matchesStats']
            summonerDataModel = summonersData[i]
            for matchStat in matchesStats:
                messages = []
                if matchStat['kills'] > 19:
                    messages.append({'name': 'Kills', 'value': matchStat["kills"]})
                if matchStat['deaths'] > 14:
                    messages.append({'name': 'Deaths (waaw!)', 'value': matchStat["deaths"]})
                if matchStat['pentaKills'] > 0:
                    messages.append({'name': 'PentaKills', 'value': matchStat["pentaKills"]})
                if matchStat['quadraKills'] > 0:
                    messages.append({'name': 'QuadraKills', 'value': matchStat["quadraKills"]})
                if matchStat['doubleKills'] > 3:
                    messages.append({'name': 'DoubleKills', 'value': matchStat["doubleKills"]})
                if matchStat['assists'] > 19:
                    messages.append({'name': 'Assists', 'value': matchStat["assists"]})
                if len(messages) > 0:
                    meta_data = self.get_match_meta_data(matchStat)
                    self.shareStatMessageInChannel(summonerDataModel.name, messages, meta_data)

    def get_match_meta_data(self, matchStat):
        fields = []
        if matchStat['queueId'] in constants.QUEUE_ID_GAME_TYPE_MAPPING:
            fields.append({'name': 'Game Type', 'value': constants.QUEUE_ID_GAME_TYPE_MAPPING[matchStat['queueId']]})
        result = {'fields': fields}
        if str(matchStat['championId']) in constants.CHAMPIONS_DATA:
            champion_data = constants.CHAMPIONS_DATA[str(matchStat['championId'])]
            fields.append({'name': 'Champion', 'value': champion_data['name']})
            icon = constants.CHAMPION_ROOT_IMAGE_PATH_URL + champion_data['icon']
            result['icon'] = icon
        return result

    def shareStatMessageInChannel(self, playerName, messages, meta_data):
        embed = discord.Embed(title='Today News!',
                              description=f'Following highlights from one of "{playerName}" games:', color=0x27966b)
        if 'icon' in meta_data:
            embed.set_thumbnail(url=meta_data['icon'])
        for data in meta_data['fields']:
            embed.add_field(name=data['name'], value=data['value'], inline=True)
        for message in messages:
            embed.add_field(name=message['name'], value=message['value'], inline=True)
        asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)

    def shareTopPlayersStatsPerCategory(self):
        topKillsSummoner = sotrageutils.getTopKillsList()[0]
        topDeathsSummoner = sotrageutils.getTopDeathsList()[0]
        topAssistsSummoner = sotrageutils.getTopAssistsList()[0]
        topFarmsSummoner = sotrageutils.getTopFarmsList()[0]
        topGamesSummoner = sotrageutils.getTopAssistsList()[0]
        topKDASummoner = sotrageutils.getTopKDAList()[0]

        embed = discord.Embed(title='Today News!',
                              description=f'All summoners stats are reseted to zeros, and below are the top summoners of previous month ({self.getPrevMonthName()}):',
                              color=0x27966b)
        self.addTopEmbedFiled(embed, 'Kills', topKillsSummoner[0], topKillsSummoner[1])
        self.addTopEmbedFiled(embed, 'Deaths', topDeathsSummoner[0], topDeathsSummoner[1])
        self.addTopEmbedFiled(embed, 'Assists', topAssistsSummoner[0], topAssistsSummoner[1])
        self.addTopEmbedFiled(embed, 'Farms', topFarmsSummoner[0], topFarmsSummoner[1])
        self.addTopEmbedFiled(embed, 'Games Count', topGamesSummoner[0], topGamesSummoner[1])
        self.addTopEmbedFiled(embed, 'Average KDA', topKDASummoner[0], topKDASummoner[1])
        asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)

    def addTopEmbedFiled(self, embed, category, summonerName, topValue):
        embed.add_field(name=f'Top {category}', value=f'{summonerName} with {topValue} {category.lower()}',
                        inline=False)

    def getPrevMonthName(self):
        month_number = datetime.today().month
        if month_number == 1:
            month_number = 12
        else:
            month_number = month_number - 1
        return calendar.month_name[month_number]
