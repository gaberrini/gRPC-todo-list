import database.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

from database.tables.TodoLists import TodoList


class Database(object):
    db_engine = create_engine(config.SQL_LITE_DATABASE_PATH)
    session_maker = scoped_session(sessionmaker(bind=db_engine, autocommit=False))

    @classmethod
    def create_db_tables(cls):
        """
        Create all tables added to the declarative_base Base
        """
        try:
            Base.metadata.create_all(cls.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error creating DB Tables - {}".format(e))

    @classmethod
    def drop_all(cls):
        """
        Drop all tables, used for testing
        """
        TodoList.__table__.drop(cls.db_engine)
