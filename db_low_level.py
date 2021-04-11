import os

from sqlalchemy import Column, Integer, Float, VARCHAR, BIGINT, create_engine, Computed
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

DB_USER = os.getenv('DBUSER')
DB_PASSWORD = os.getenv('DBPASSWORD')
DB_HOST = os.getenv('DBHOST')
DB_MAIN_NAME = os.getenv('DBMAINDB')

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_MAIN_NAME}', poolclass=NullPool)
Base = declarative_base()


class SummonerData(Base):
    __tablename__ = 'SummonersData'
    accountId = Column(VARCHAR(100), primary_key=True)
    name = Column(VARCHAR(30), unique=True, nullable=False)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    lastGameTimeStamp = Column(BIGINT, default=0)  # current time stamp...
    avg_kda = Column(Float, default=0.0)
    farms = Column(Integer, default=0)
    total_games = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    loses = Column(Integer, default=0)
    win_rate = Column(VARCHAR(10),
                      Computed('CONCAT(ROUND(((wins / IF((wins + loses) = 0, 1, (wins + loses))) * 100), 2), "%")'),
                      default=0)


class CommonTable(Base):
    __tablename__ = 'CommonTable'
    key = Column(VARCHAR(20), primary_key=True)
    value = Column(VARCHAR(20), nullable=False)


Base.metadata.create_all(engine)
