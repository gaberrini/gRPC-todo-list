"""
TodoList DB Table definition, extending src.database.database.Base, this way
it will be automatically created when src.database.database.Database.create_db_tables is executed.

Classes:
    TodoList(db.Base)
"""
from sqlalchemy import Column, Integer, String
import database.database as db


class TodoList(db.Base):  # pylint: disable=too-few-public-methods
    """
    TodoList DB Table definition

    Attributes:
        TodoList.__tablename__ (str): DB Table name
        TodoList.id (sqlalchemy.Column): ID primary_key column
        TodoList.name (sqlalchemy.Column): List name column
    """
    __tablename__ = 'todo-lists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False, unique=True)

    def __init__(self, name: str):
        """
        Constructor to create new TodoList entry

        :param name: New List name
        """
        self.name = name

    def __repr__(self):
        """
        String representation of the list

        :return:
        """
        return '{}-{}'.format(self.id, self.name)
