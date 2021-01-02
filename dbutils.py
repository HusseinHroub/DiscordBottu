from replit import db
SUMMONER_PREFIX = '[Sum[Col'
ACCOUNT_PREFIX = '[Acc[id'

def getSummonerValue(summonerName):
  return getValue(SUMMONER_PREFIX + summonerName)

def getAccountValue(account_id):
  return getValue(ACCOUNT_PREFIX + account_id)

def setSummonerValue(summonerName, account_id):
  setValue(SUMMONER_PREFIX + summonerName, account_id)

def setAccountValue(account_id, value):
  setValue(ACCOUNT_PREFIX + account_id, value)

def getValue(key):
  try:
    return db[key]
  except KeyError:
    return None

def setValue(key, value):
  db[key] = value

def deleteKey(key):
  del db[key]



