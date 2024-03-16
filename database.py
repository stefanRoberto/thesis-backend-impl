import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USERNAME = settings.database['USERNAME']
DB_PASSWORD = settings.database['PASSWORD']
DB_HOST = settings.database['HOST']
DB_PORT = settings.database['PORT']
DB_NAME = settings.database['NAME']

DB_URL = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}[:{DB_PORT}]/{DB_NAME}'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
