"""
Database service functions
"""
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database

from app.config import settings
from app.database import Base, Session


def init_database():
    if not database_exists(settings.sqlalchemy_database_uri):
        create_database(settings.sqlalchemy_database_uri)
    elif settings.dev_mode and settings.drop_db:
        drop_database(settings.sqlalchemy_database_uri)
        create_database(settings.sqlalchemy_database_uri)

    engine = create_engine(settings.sqlalchemy_database_uri)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return
