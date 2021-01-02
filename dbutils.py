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
    return myresult != None and len(myresult) == 1
  
class InsertSummonerQuery:
  def __init__(self, accountId, summonerName):
    self.accountId = accountId
    self.summonerName = summonerName

  def execute(self, mydb):
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {TABLE_NAME} VALUES (%s, %s, %s, %s, %s)"
    val = (self.accountId, self.summonerName, 0, 0, 0)
    mycursor.execute(sql, val)
    mydb.commit()

class GetSummonersOrderedByStatQuery:
  def __init__(self, stats):
    self.stats = stats

  def execute(self, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {NAME}, {self.stats} FROM {TABLE_NAME} ORDER BY {self.stats} DESC")
    return mycursor.fetchall()

def connectionWrapper(queryExecutor):
  mydb = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_MAIN_NAME)
  response = queryExecutor.execute(mydb)
  mydb.close()
  return response

def isSummonerExist(summonerName):
  return connectionWrapper(SummonerExistQuery(summonerName))

def insertSummoner(accountId, summonerName):
  return connectionWrapper(InsertSummonerQuery(accountId, summonerName))

def getSummonerSortedByStat(stats):
   return connectionWrapper(GetSummonersOrderedByStatQuery(stats))
