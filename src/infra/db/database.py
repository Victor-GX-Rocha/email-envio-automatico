""" Base for database conections. """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import AppConfigManager

config = AppConfigManager()

url: str = config.database_url

engine = create_engine(url)
Base = declarative_base()
InternalSession = sessionmaker(bind=engine)

def init_database():
    """ Start the database. """
    Base.metadata.create_all(engine)
    print("Starting database")
