from sqlalchemy import Table, Column, Integer, Numeric, String, Text, ForeignKey, DateTime, MetaData, create_engine, desc, func, cast, and_, or_, not_, BigInteger, Boolean, Float, exists, DATE
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from datetime import datetime

# DB Connection
user = 'user'
password = 'jayapura'
host = 'localhost'
#host = '192.168.0.69'
port = 5432
dbTraffic = 'tr4ff1c'
dbSource = 's0urc3'
dbRaw = 's0urc3'
dbProcessing = 'pr0c3ss1ng'

urlPostgres = 'postgresql://{}:{}@{}:{}/{}'

urlPostgresRaw = urlPostgres.format(user, password, host, port, dbRaw)
urlPostgresProcessing = urlPostgres.format(user, password, host, port, dbProcessing)
urlPostgresTraffic = urlPostgres.format(user, password, host, port, dbTraffic)

enginePostgresRaw = create_engine(urlPostgresRaw, client_encoding='utf-8')
enginePostgresProcessing = create_engine(urlPostgresProcessing, client_encoding='utf-8')
enginePostgresTraffic = create_engine(urlPostgresTraffic, client_encoding='utf-8')

SessionPostgresRaw = sessionmaker(bind=enginePostgresRaw)
sessionPostgresRaw = SessionPostgresRaw()
BasePostgresRaw = declarative_base()

SessionPostgresProcessing = sessionmaker(bind=enginePostgresProcessing)
sessionPostgresProcessing = SessionPostgresProcessing()
BasePostgresProcessing = declarative_base()

SessionPostgresTraffic = sessionmaker(bind=enginePostgresTraffic)
sessionPostgresTraffic = SessionPostgresTraffic()
BasePostgresTraffic = declarative_base()

#db = 'tr4ff1c'
urlMysql = 'mysql+pymysql://{}:{}@{}/{}'

urlMysqlTraffic = urlMysql.format(user, password, host, dbTraffic)

urlMysqlSource = urlMysql.format(user, password, host, dbSource)

engineMysqlTraffic = create_engine(urlMysqlTraffic)

engineMysqlSource = create_engine(urlMysqlSource)

SessionMysqlTraffic = sessionmaker(bind=engineMysqlTraffic)
sessionMysqlTraffic = SessionMysqlTraffic()
BaseMysqlTraffic = declarative_base()

SessionMysqlSource = sessionmaker(bind=engineMysqlSource)
sessionMysqlSource = SessionMysqlSource()
BaseMysqlSource = declarative_base()

# DB Table
class Raw(BasePostgresRaw):
    __tablename__ = 'raws'
    id = Column(BigInteger, primary_key=True)
    respondent_id = Column(BigInteger(), default=30) # SbyTraffiServ
    tweetID = Column(BigInteger())
    tweetTime = Column(DateTime())
    tweetUID = Column(BigInteger())
    tweetUScreenName = Column(String(255))
    info = Column(Text())
    url = Column(String(255))
    media = Column(String(255))
    mediaWidth = Column(Integer())
    mediaHeight = Column(Integer())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    machineClassification = Column(Integer(), default=1) # HAM
    humanClassification = Column(Integer(), default=1) # HAM
    isProcessed = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class Machine(BasePostgresProcessing):
    __tablename__ = 'machines'
    id = Column(BigInteger, primary_key=True)
    raw_id = Column(BigInteger())
    classification_id = Column(Integer())
    place_id = Column(BigInteger())
    category_id = Column(Integer())
    weather_id = Column(Integer())
    spot_id = Column(BigInteger())
    tweetID = Column(BigInteger())
    info = Column(String(255))
    image = Column(String(255))
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    isExported = Column(Boolean, unique=False, default=False)
    isOfficial = Column(Boolean, unique=False, default=True)
    active = Column(Boolean, unique=False, default=True)

class Source(BaseMysqlSource):
    __tablename__ = 'sources'
    id = Column(BigInteger, primary_key=True)
    respondent_id = Column(Integer())
    twitID = Column(BigInteger())
    twitTime = Column(DateTime())
    twitUserID = Column(BigInteger())
    twitUScreenName = Column(String(255))
    info = Column(Text())
    url = Column(String(255))
    media = Column(String(255))
    #created = Column(DateTime(), default=datetime.now)
    #modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    active = Column(Boolean, unique=False, default=True)

# DB Table
class PlaceMysql(BaseMysqlTraffic):
    __tablename__ = 'places'
    id = Column(BigInteger, primary_key=True)
    region_id = Column(Integer())
    name = Column(String(255))
    lat = Column(Float())
    lng = Column(Float())
    active = Column(Boolean, unique=False, default=True)

class PlacePostgres(BasePostgresTraffic):
    __tablename__ = 'places'
    id = Column(BigInteger, primary_key=True)
    regency_id = Column(Integer())
    name = Column(String(255))
    lat = Column(Float())
    lng = Column(Float())
    active = Column(Boolean, unique=False, default=True)

class RegionMysql(BaseMysqlTraffic):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    lat = Column(Float())
    lng = Column(Float())
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class RegionPostgres(BasePostgresTraffic):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    lat = Column(Float())
    lng = Column(Float())
    name = Column(String(255))
    description = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class RespondentPostgres(BasePostgresTraffic):
    __tablename__ = 'respondents'
    id = Column(BigInteger, primary_key=True)
    region_id = Column(Integer())
    twitterUID = Column(BigInteger())
    name = Column(String(255))
    contact = Column(String(255))
    isOfficial = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class RespondentMysql(BaseMysqlTraffic):
    __tablename__ = 'respondents'
    id = Column(BigInteger, primary_key=True)
    region_id = Column(Integer())
    twitUserID = Column(BigInteger())
    name = Column(String(255))
    contact = Column(String(255))
    isOfficial = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class UserPostgres(BasePostgresTraffic):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    group_id = Column(Integer())
    region_id = Column(Integer())
    tweetUID = Column(BigInteger())
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class StatePostgres(BasePostgresTraffic):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class StateMysql(BaseMysqlTraffic):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class RegencyPostgres(BasePostgresTraffic):
    __tablename__ = 'regencies'
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer())
    hierarchy_id = Column(Integer())
    name = Column(String(255))
    alias = Column(String(255))
    lat = Column(Float())
    lng = Column(Float())
    active = Column(Boolean, unique=False, default=True)

class RegencyMyql(BaseMysqlTraffic):
    __tablename__ = 'regencies'
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer())
    region_id = Column(Integer())
    hierarchy_id = Column(Integer())
    name = Column(String(255))
    lat = Column(Float())
    lng = Column(Float())
    active = Column(Boolean, unique=False, default=True)

class DistrictPostgres(BasePostgresTraffic):
    __tablename__ = 'districts'
    id = Column(Integer, primary_key=True)
    regency_id = Column(Integer())
    name = Column(String(255))
    lat = Column(Float(), default=None)
    lng = Column(Float(), default=None)
    active = Column(Boolean, unique=False, default=True)

class HierarchyPostgres(BasePostgresTraffic):
    __tablename__ = 'hierarchies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class RegencyRegionPostgres(BasePostgresTraffic):
    __tablename__ = 'regencies_regions'
    id = Column(Integer, primary_key=True)
    regency_id = Column(Integer())
    region_id = Column(Integer())
    active = Column(Boolean, unique=False, default=True)

class WeatherPostgres(BasePostgresTraffic):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class WeatherMysql(BaseMysqlTraffic):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class CategoryMysql(BaseMysqlTraffic):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class CategoryPostgres(BasePostgresTraffic):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    active = Column(Boolean, unique=False, default=True)

class KindPostgres(BasePostgresProcessing):
    __tablename__ = 'kinds'
    id = Column(BigInteger, primary_key=True)
    raw_id = Column(BigInteger())
    tweetID = Column(BigInteger())
    classification_id = Column(Integer())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    isProcessed = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class ChunkPostgres(BasePostgresProcessing):
    __tablename__ = 'chunks'
    id = Column(BigInteger, primary_key=True)
    tweetID = Column(BigInteger())
    placeName = Column(String(255))
    conditionName = Column(String(255))
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    isProcessed = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class SpotPostgres(BasePostgresProcessing):
    __tablename__ = 'spots'
    id = Column(BigInteger, primary_key=True)
    chunk_id = Column(BigInteger())
    tweetID = Column(BigInteger())
    place_id = Column(BigInteger())
    category_id = Column(Integer())
    score = Column(Float())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    isProcessed = Column(Boolean, unique=False, default=False)
    active = Column(Boolean, unique=False, default=True)

class FailPostgres(BasePostgresProcessing):
    __tablename__ = 'fails'
    id = Column(BigInteger, primary_key=True)
    raw_id = Column(BigInteger())
    error_id = Column(Integer())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    active = Column(Boolean, unique=False, default=True)

class MarkerPostgres(BasePostgresTraffic):
    __tablename__ = 'markers'
    id = Column(BigInteger, primary_key=True)
    category_id = Column(Integer())
    user_id = Column(BigInteger())
    respondent_id = Column(BigInteger())
    weather_id = Column(Integer())
    source_id = Column(BigInteger())
    lat = Column(Float())
    lng = Column(Float())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    info = Column(Text(), default=None)
    isPinned = Column(Boolean, default=False)
    isCleared = Column(Boolean, default=False)
    isExported = Column(Boolean, default=False)
    active = Column(Boolean, unique=False, default=True)

class MarkerMysql(BaseMysqlTraffic):
    __tablename__ = 'markers'
    id = Column(BigInteger, primary_key=True)
    category_id = Column(Integer())
    user_id = Column(BigInteger())
    respondent_id = Column(BigInteger())
    weather_id = Column(Integer())
    lat = Column(Float())
    lng = Column(Float())
    created = Column(DateTime(), default=datetime.now)
    modified = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    info = Column(Text(), default=None)
    twitID = Column(BigInteger())
    twitPlaceID = Column(String(255), default=None)
    twitTime = Column(DateTime())
    twitURL = Column(String(255), default=None)
    twitPlaceName = Column(String(255), default=None)
    isTwitPlacePrecise = Column(Boolean, default=False)
    twitImage = Column(String(255), default=None)
    pinned = Column(Boolean, default=False)
    cleared = Column(Boolean, default=False)
    active = Column(Boolean, unique=False, default=True)
