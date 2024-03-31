from settings import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3306

DB_URL = (f'mysql+mysqlconnector://{database["USERNAME"]}:{database["PASSWORD"]}'
          f'@{database["HOST"] or DEFAULT_HOST}:{database["PORT"] or DEFAULT_PORT}/{database["NAME"]}')

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database():
    return Base.metadata.create_all(bind=engine)


def drop_database():
    return Base.metadata.drop_all(bind=engine)


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
