import certifi
import pymongo
from src.database.base_dao import BaseDAO
from src.config.config import config

client = pymongo.MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
work_days_api_dao = BaseDAO(client, config.MONGO_DBNAME, 'workday_api')
work_days_beautifulsoup_dao_1 = BaseDAO(client, config.MONGO_DBNAME, 'workday_beautifulsoup')
work_days_beautifulsoup_dao = BaseDAO(client, config.MONGO_DBNAME, 'workday_beautifulsoup_test')
