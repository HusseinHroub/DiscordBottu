import dbutils
from lolutils import lolApiUtils
from queue import Queue
from threading import Thread
import sotrageutils
from statsUtils import lolStatsMerger
import traceback
import discord
import asyncio

class LolStatUpdatorTask:
  def __init__(self, channel, loop):
    self.channel = channel
    self.loop = loop

  def execute(self):
    summonersData = dbutils.getAllSummonerData()
    results = self.getSummonersStats(summonersData)
    newSummonersData = self.getNewSummonerData(summonersData, results)
    self.updateToDBIfNotEmptyData(newSummonersData)
    self.shareAnnouncmentMessagesInDB(results, summonersData)
    
  def getSummonersStats(self, summonersData):
    queue = Queue(maxsize=0)
    numberOfThreads = min(30, len(summonersData))
    results = [None for x in summonersData];
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
      summonerData = work[1]
      matches = lolApiUtils.getMatchesByAccountId(summonerData[0], summonerData[4])
      if matches != None and len(matches) > 0:
        try: 
          matches_stats = lolApiUtils.getMatchesStats(matches, summonerData[0])
          matches_merged_stat = lolStatsMerger.mergeGamesStats(matches_stats)
          result = {
            **matches_merged_stat,
            'lastGameTimeStamp': matches[0]['timestamp'] + 1,
            'accountId': summonerData[0]
          }
          results[work[0]] = {'totalStatsResult': result, 'matchesStats': matches_stats}
        except:
          print('error happened while updating player stats!')
          traceback.print_exc()
      
  def getNewSummonerData(self, summonersData, results):
    newSummonersData = []
    for i in range(len(summonersData)):
      if results[i] == None:
        continue
      result = results[i]['totalStatsResult']
      summonerData = summonersData[i]
      newSummonersData.append({
        'kills': result['total_kills'] + summonerData[1],
        'deaths': result['total_deaths'] + summonerData[2],
        'assists': result['total_assists'] + summonerData[3],
        'farms': result['total_farms'] + summonerData[5],
        'accountId': summonerData[0],
        'lastGameTimeStamp': result['lastGameTimeStamp'],
        **self.getKDAInfo(result['avg_kda'], summonerData[6], result['sample_count'], summonerData[7])
      })
    return newSummonersData
    
  def getKDAInfo(self, newKDA, oldKda, newCount, oldCount):
    totalCount = newCount + oldCount
    return {
     'avgKda': oldKda + (newKDA - oldKda) / totalCount,
     'totalGames': totalCount
     }

  def updateToDBIfNotEmptyData(self, newSummonersData):
    if newSummonersData != None and len(newSummonersData) > 0:
      print('updating db!')
      dbutils.updateSummonersData(newSummonersData)
      sotrageutils.updateCache()
  
  def shareAnnouncmentMessagesInDB(self, results, summonersData):
    for i in range(len(results)):
      if results[i] == None:
        continue
      matchesStats = results[i]['matchesStats']
      summonerData = summonersData[i]
      for matchStat in matchesStats:
        message = ''
        if matchStat['kills'] > 19:
          message += f'{matchStat["kills"]} Kills!\n'
        if matchStat['deaths'] > 14:
          message += f'{matchStat["deaths"]} Deaths! [waaaaw..]\n'
        if matchStat['pentaKills'] > 0:
          message += f'{matchStat["pentaKills"]} PentaKills!\n'
        if matchStat['quadraKills'] > 0:
          message += f'{matchStat["quadraKills"]} QuadraKills!\n'
        if matchStat['doubleKills'] > 3:
          message += f'{matchStat["doubleKills"]} DoubleKills!\n'
        if matchStat['assists'] > 19:
          message += f'{matchStat["assists"]} Assists!\n'
        if len(message) != '':
          self.shareStatMessageInChannel(summonerData[8], message)

  def shareStatMessageInChannel(self, playerName, message):
    embed=discord.Embed(description=f'One of {playerName} games he got:\n{message}', color=0x27966b)
    asyncio.run_coroutine_threadsafe(self.channel.send(embed=embed), self.loop)
      