import mysql.connector
import os
TABLE_NAME = 'SummonerData'
ACCOUNT_ID = 'accountId'
NAME = 'name'
KILLS = 'kills'
DEATHS = 'deaths'
ASSISTS = 'assists'
LAST_GAME_TIME_STAMP = 'lastGameTimeStamp'
FARMS = 'farms'
AVG_KDA = 'avg_kda'
TOTAL_GAMES = 'total_games'

COMMON_TABLE_NAME = 'CommonTable'
KEY = 'common_key'
VALUE = 'common_value'

DB_USER = os.getenv('DBUSER')
DB_PASSWORD = os.getenv('DBPASSWORD')
DB_HOST = os.getenv('DBHOST')
DB_MAIN_NAME = os.getenv('DBMAINDB')

class SummonerExistQuery:
  def __init__(self, summonerName):
    self.summonerName = summonerName

  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {NAME} FROM {TABLE_NAME} WHERE LOWER({NAME}) = '{self.summonerName}'")
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult != None and len(myresult) == 1
  
class AccountIdExistQuery:
  def __init__(self, accountId):
    self.accountId = accountId

  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {ACCOUNT_ID} FROM {TABLE_NAME} WHERE {ACCOUNT_ID} = '{self.accountId}'")
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult != None and len(myresult) == 1

class InsertSummonerQuery:
  def __init__(self, accountId, summonerName, kills, deaths, assists, lastGameTimeStamp, farms, avgKda, numberOfGames):
    self.accountId = accountId
    self.summonerName = summonerName
    self.kills = kills
    self.deaths = deaths
    self.assists = assists
    self.lastGameTimeStamp = lastGameTimeStamp
    self.farms = farms
    self.avgKda = avgKda
    self.numberOfGames = numberOfGames

  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {TABLE_NAME} ({ACCOUNT_ID}, {NAME}, {KILLS}, {DEATHS}, {ASSISTS}, {FARMS}, {AVG_KDA}, {TOTAL_GAMES}, {LAST_GAME_TIME_STAMP}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (self.accountId, self.summonerName, self.kills, self.deaths, self.assists, self.farms, self.avgKda, self.numberOfGames, self.lastGameTimeStamp)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

class GetSummonersOrderedByStatQuery:
  def __init__(self, stats, desc):
    self.stats = stats
    self.desc = desc

  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {NAME}, {self.stats} FROM {TABLE_NAME} ORDER BY {self.stats} {'DESC' if self.desc else 'ASC'}")
    data = mycursor.fetchall()
    mycursor.close()
    return data

class GetAllSummonerDataQuery:
  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {ACCOUNT_ID}, {KILLS}, {DEATHS}, {ASSISTS}, {LAST_GAME_TIME_STAMP}, {FARMS}, {AVG_KDA}, {TOTAL_GAMES}, {NAME} FROM {TABLE_NAME}")
    data = mycursor.fetchall()
    mycursor.close()
    return data

class UpdateSummonersDataQuery:
  def __init__(self, summonersData):
   self.summonersData = summonersData

  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"UPDATE {TABLE_NAME} SET {KILLS} = %s, {DEATHS} = %s, {ASSISTS} = %s , {LAST_GAME_TIME_STAMP} = %s, {FARMS} = %s, {AVG_KDA} = %s, {TOTAL_GAMES} = %s WHERE {ACCOUNT_ID} = %s"
    values = []
    for summonerData in self.summonersData:
      values.append((summonerData['kills'], summonerData['deaths'], summonerData['assists'], summonerData['lastGameTimeStamp'], summonerData['farms'], summonerData['avgKda'], summonerData['totalGames'], summonerData['accountId']))
    mycursor.executemany(sql, values)
    mydb.commit()
    mycursor.close()

class GetRecentTopPlayerQuery:
    def execute(self, mydb):
      mycursor = mydb.cursor()
      mycursor.execute(f"SELECT {VALUE} FROM {COMMON_TABLE_NAME} WHERE {KEY} = 'recentTopSummoner'")
      data = mycursor.fetchone()
      mycursor.close()
      return data

class UpdateRecentTopSummonerQuery:
  def __init__(self, summonerName):
    self.summonerName = summonerName
   
  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"UPDATE {COMMON_TABLE_NAME} SET {VALUE} = %s WHERE {KEY} = 'recentTopSummoner'"
    val = (self.summonerName,)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()  

class UpdateSummonerByAccountIdQuery:
  def __init__(self, accountId, summonerName):
   self.accountId = accountId
   self.summonerName = summonerName

  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"UPDATE {TABLE_NAME} SET {NAME} = %s WHERE {ACCOUNT_ID} = %s"
    val = (self.summonerName, self.accountId)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

def connectionWrapper(queryExecutor):
  mydb = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_MAIN_NAME)
  response = queryExecutor.execute(mydb)
  mydb.close()
  return response

def isSummonerExist(summonerName):
  return connectionWrapper(SummonerExistQuery(summonerName))

def isAccountIdExist(accountId):
  return connectionWrapper(AccountIdExistQuery(accountId))

def insertSummoner(accountId, summonerName, kills, deaths, assists, lastGameTimeStamp, farms, avgKda, numberOfGames):
  return connectionWrapper(InsertSummonerQuery(accountId, summonerName, kills, deaths, assists, lastGameTimeStamp, farms, avgKda, numberOfGames))

def getSummonersSortedByStat(stats, desc = True):
   return connectionWrapper(GetSummonersOrderedByStatQuery(stats, desc))

def getAllSummonerData():
  return connectionWrapper(GetAllSummonerDataQuery())

def updateSummonerByAccountId(accountId, summonerName = None):
  return connectionWrapper(UpdateSummonerByAccountIdQuery(accountId, summonerName))
  
def updateSummonersData(summonersData):
  return connectionWrapper(UpdateSummonersDataQuery(summonersData))

def getRecentTopPlayer():
  return connectionWrapper(GetRecentTopPlayerQuery())

def updateRecentTopPlayer(summonerName):
  connectionWrapper(UpdateRecentTopSummonerQuery(summonerName))