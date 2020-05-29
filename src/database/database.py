import database.config as config
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

import database.tables.TodoLists as TodoLists


class Database(object):

    def __init__(self):
        self.db_engine = create_engine(config.SQL_LITE_DATABASE_PATH)
        session_maker = sessionmaker(bind=self.db_engine, autocommit=False)
        self.session_maker = scoped_session(session_maker)

    def create_db_tables(self):
        try:
            Base.metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error creating DB Tables - {}".format(e))

    def new_todo_list_entry(self, name: str) -> Optional[int]:
        """
        Create a new todoList entry in the database

        :param name:
        :return: New todoList entry id
        """
        try:
            session = self.session_maker()
            new_todo_list = TodoLists.TodoList(name=name)
            session.add(new_todo_list)
            session.commit()
            new_id = new_todo_list.id
            return new_id
        except IntegrityError as e:
            print('TodoList name must be unique. List with name "{}" already exist'.format(name))
            raise e
        except Exception as e:
            print('Error creating new todo list entry - {}'.format(e))
            raise e
        finally:
            self.session_maker.remove()

    def drop_all(self):
        """
        Drop all tables, used for testing
        """
        TodoLists.TodoList.__table__.drop(self.db_engine)
