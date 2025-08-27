import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # mongoDB config
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI').format(MONGO_DBNAME=MONGO_DBNAME)


config = Config()
