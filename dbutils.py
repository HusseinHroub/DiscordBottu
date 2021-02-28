from typing import List

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from db_low_level import engine, SummonerData, CommonTable
from models import SummonerDataModel

Session = sessionmaker(bind=engine)


def SessionManager(func):
    def wrap(*args):
        session = Session()
        try:
            result = func(*args, session=session)
            session.commit()
            return result
        except:
            session.rollback()
            raise
        finally:
            session.close()

    return wrap


def isSummonerNameExist(summonerName, session):
    return session.query(func.count(SummonerData.name)).filter_by(name=summonerName).scalar() == 1


def isAccountIdExist(accountId, session):
    return session.query(func.count(SummonerData.accountId)).filter_by(accountId=accountId).scalar() == 1


def insertSummoner(accountId, summonerName, lastGameTimeStamp, session):
    summonerData = SummonerData(accountId=accountId,
                                name=summonerName,
                                lastGameTimeStamp=lastGameTimeStamp)
    session.add(summonerData)


def getSummonersSortedByStat(stats, desc=True, session=None) -> List[SummonerDataModel]:
    statsColumn = SummonerData.__dict__[stats]
    return session.query(SummonerData.name, statsColumn).order_by(
        statsColumn.desc() if desc else statsColumn.asc()).all()


def getAllSummonerData(session) -> List[SummonerDataModel]:
    return convertListOfDataToModels(session.query(SummonerData).all())


def updateSummonerNameByAccountId(accountId, summonerName=None, session=None):
    session.query(SummonerData).filter(SummonerData.accountId == accountId).update({'name': summonerName})


def getCommonTableValue(key, session):
    return session.query(CommonTable.value).filter_by(key=key).one().value


def updateCommonTableRow(key, value, session):
    session.query(CommonTable).filter(CommonTable.key == key).update({'value': value})


def resetStats(session):
    session.query(SummonerData).update(
        {'kills': 0, 'deaths': 0, 'assists': 0, 'farms': 0, 'avg_kda': 0, 'total_games': 0})


def convertListOfDataToModels(listOfData):
    models = []
    for data in listOfData:
        model = SummonerDataModel()
        model.buildWithDataObject(data)
        models.append(model)
    return models
