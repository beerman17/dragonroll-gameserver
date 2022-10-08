"""
Database service functions
"""
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database

from app.config import settings
from app.database import Base, Session


def init_database():
    if not database_exists(settings.db_uri):
        create_database(settings.db_uri)
    elif settings.dev_mode and settings.drop_db:
        drop_database(settings.db_uri)
        create_database(settings.db_uri)

    engine = create_engine(settings.db_uri)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return
