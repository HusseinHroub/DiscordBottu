import mysql.connector
import os
TABLE_NAME = 'SummonerData'
ACCOUNT_ID = 'accountId'
NAME = 'name'

DB_USER = os.getenv('DBUSER')
DB_PASSWORD = os.getenv('DBPASSWORD')
DB_HOST = os.getenv('DBHOST')
DB_MAIN_NAME = os.getenv('DBMAINDB')

class SummonerExistQuery:
  def __init__(self, summonerName):
    self.summonerName = summonerName

  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {NAME} FROM {TABLE_NAME} WHERE {NAME} = '{self.summonerName}'")
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult != None and len(myresult) == 1
  
class InsertSummonerQuery:
  def __init__(self, accountId, summonerName, kills, deaths, assists, lastGameTimeStamp):
    self.accountId = accountId
    self.summonerName = summonerName
    self.kills = kills
    self.deaths = deaths
    self.assists = assists
    self.lastGameTimeStamp = lastGameTimeStamp

  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {TABLE_NAME} VALUES (%s, %s, %s, %s, %s, %s)"
    val = (self.accountId, self.summonerName, self.kills, self.deaths, self.assists, self.lastGameTimeStamp)
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

def connectionWrapper(queryExecutor):
  mydb = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_MAIN_NAME)
  response = queryExecutor.execute(mydb)
  mydb.close()
  return response

def isSummonerExist(summonerName):
  return connectionWrapper(SummonerExistQuery(summonerName))

def insertSummoner(accountId, summonerName, kills, deaths, assists, lastGameTimeStamp):
  return connectionWrapper(InsertSummonerQuery(accountId, summonerName, kills, deaths, assists, lastGameTimeStamp))

def getSummonersSortedByStat(stats, desc):
   return connectionWrapper(GetSummonersOrderedByStatQuery(stats, desc))
