"""
This module contains the Database handler and the sqlalchemy DeclarativeMeta class to be used
as base class when defining the DB tables as classes and be able to use the ORM.

Attributes:
    Base (sqlalchemy.ext.declarative.api.DeclarativeMeta): Base Class to declare DB tables and generate an ORM

Classes:
    Database(object)
"""
import database.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()

from database.tables.TodoLists import TodoList


class Database(object):
    """
    Database base class, extended by database handlers for the different tables

    Attributes:
            Database.db_engine (sqlalchemy.engine.base.Engine): Engine used to create DB Sessions
            Database.session_maker (sqlalchemy.orm.scoping.scoped_session): Scoped session manager
    """

    db_engine = create_engine(config.SQL_LITE_DATABASE_PATH)
    session_maker = scoped_session(sessionmaker(bind=db_engine, autocommit=False))

    @classmethod
    def create_db_tables(cls):
        """
        Create all DB tables added to the declarative_base Base
        """
        print("Creating DB tables")
        Base.metadata.create_all(cls.db_engine)

    @classmethod
    def drop_all(cls):
        """
        Drop all tables, used for testing
        """
        TodoList.__table__.drop(cls.db_engine)
