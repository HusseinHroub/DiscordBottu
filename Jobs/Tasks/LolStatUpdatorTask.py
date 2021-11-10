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
from statsUtils import lolStatsMerger, stat_helper_utils


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
                self.finalizeMonthStats(session)
        else:
            if sotrageutils.getMonthAnnouncedValue() == 'True':
                sotrageutils.markMonthAnnouncedValue('False', session)
                session.commit()

    def finalizeMonthStats(self, session):
        self.shareTopPlayersStatsPerCategory()
        dbutils.resetStats(session)
        sotrageutils.markMonthAnnouncedValue('True', session)
        sotrageutils.updateStatCache(session)
        session.commit()

    def startUpdateProcess(self, session):
        summonersDatabaseResults = dbutils.getAllSummonerData(session)
        session.close()
        summonersLolAPIResults = self.getSummonersAPIStats(summonersDatabaseResults)
        summonersMergedResults = self.mergeSummonersDataBaseAndAPIResults(summonersDatabaseResults,
                                                                          summonersLolAPIResults)
        self.updateToDBIfNotEmptyData(summonersMergedResults, session)
        self.shareSummonersMatchesStatsIfDeserved(summonersLolAPIResults, summonersDatabaseResults)

    def getSummonersAPIStats(self, summonersData):
        queue = Queue(maxsize=0)
        numberOfThreads = 1
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
                    results[work[0]] = self.getSummonerMatchesData(matches, summonerDataModel.accountId)
                except:
                    print(
                        f'error happened while getting total stats of player with accountId: {summonerDataModel.accountId}')
                    traceback.print_exc()

    def getSummonerMatchesData(self, matches, accountId):
        matches_stats = lolApiUtils.getMatchesStats(matches, accountId)
        if len(matches_stats) == 0:
            return None
        matches_merged_stat = lolStatsMerger.mergeGamesStats(matches_stats)
        result = {
            **matches_merged_stat,
            'lastGameTimeStamp': (matches_stats[0]['gameEndTimestamp'] / 1000) + 1,
            'accountId': accountId
        }
        return {'totalStatsResult': result, 'matchesStats': matches_stats}

    def mergeSummonersDataBaseAndAPIResults(self, summonersData, results):
        newSummonersData = []
        for i in range(len(summonersData)):
            if results[i] == None:
                continue
            newSummonersData.append(
                self.mergeAPIResultAndSummonerDataModel(results[i]['totalStatsResult'], summonersData[i]))
        return newSummonersData

    def mergeAPIResultAndSummonerDataModel(self, result, summonerDataModel):
        merged_results = {'accountId': summonerDataModel.accountId, 'lastGameTimeStamp': result['lastGameTimeStamp']}
        for statHelper in stat_helper_utils.stat_helpers:
            merged_results.update(statHelper.mergeResultWithSummonerData(result, summonerDataModel))
        return merged_results

    def updateToDBIfNotEmptyData(self, newSummonersData, session):
        if newSummonersData != None and len(newSummonersData) > 0:
            print('updating db!')
            session.bulk_update_mappings(dbutils.SummonerData, newSummonersData)
            sotrageutils.updateStatCache(session)

    def shareSummonersMatchesStatsIfDeserved(self, results, summonersData):
        for i in range(len(results)):
            if results[i] == None:
                continue
            matchesStats = results[i]['matchesStats']
            summonerDataModel = summonersData[i]
            for matchStat in matchesStats:
                self.shareSummonerStatsIfDeserveAnAnnounce(matchStat, summonerDataModel.name)

    def shareSummonerStatsIfDeserveAnAnnounce(self, matchStat, name):
        statsNameAndValue = self.getStatsNameAndValueToBeAnnounced(matchStat)
        if len(statsNameAndValue) > 0:
            meta_data = self.get_match_meta_data(matchStat)
            self.shareStatMessageInChannel(name, statsNameAndValue, meta_data)

    def getStatsNameAndValueToBeAnnounced(self, matchStat):
        messages = []
        for statHelper in stat_helper_utils.stat_helpers:
            if statHelper.isEligibleForAnnouncment(matchStat):
                messages.append(statHelper.getAnnouncmentNameValue(matchStat))
        if matchStat['pentaKills'] > 0:
            messages.append({'name': 'PentaKills', 'value': matchStat["pentaKills"]})
        if matchStat['quadraKills'] > 0:
            messages.append({'name': 'QuadraKills', 'value': matchStat["quadraKills"]})
        if matchStat['doubleKills'] > 3:
            messages.append({'name': 'DoubleKills', 'value': matchStat["doubleKills"]})
        return messages

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
        embed = discord.Embed(title='Today News!',
                              description=f'All summoners stats are reseted to zeros, and below are the top summoners of previous month ({self.getPrevMonthName()}):',
                              color=0x27966b)
        for statHelper in stat_helper_utils.stat_helpers:
            statHelper.addFieldToTopEmbed(embed)
        asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)

    def getPrevMonthName(self):
        month_number = datetime.today().month
        if month_number == 1:
            month_number = 12
        else:
            month_number = month_number - 1
        return calendar.month_name[month_number]
