"""
This module contains the class to interact with the TodoList DB table.

Classes:
    TodoListDBHandler(Database)
"""
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from database.database import Database
from database.tables.todo_lists import TodoList


class TodoListDBHandler(Database):
    """
    TodoList DB table Handler
    """

    @classmethod
    def new_todo_list_entry(cls, name: str) -> Optional[int]:
        """
        Create a new todoList entry in the database

        :param name: New list name

        :return: New todoList ID

        :raise IntegrityError: If List with `name` already exist in the DB
        """
        try:
            session = cls.session_maker()
            new_todo_list = TodoList(name=name)
            session.add(new_todo_list)
            session.commit()
            new_id = new_todo_list.id
            return new_id
        except IntegrityError as ex:
            print('TodoList name must be unique. List with name "{}" already exist'.format(name))
            raise ex
        finally:
            cls.session_maker.remove()

    @classmethod
    def get_all(cls) -> List[TodoList]:
        """
        :return: All TodoLists DB entries
        """
        try:
            session = cls.session_maker()
            return session.query(TodoList).all()
        finally:
            cls.session_maker.remove()
