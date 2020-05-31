"""
This module contains the class to interact with the TodoList DB table.

Classes:
    TodoListDBHandler(Database)
"""
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from config.config import MAX_PAGE_SIZE
from database.database import Database
from database.tables.todo_lists import TodoList


class TodoListDBHandler(Database):
    """
    TodoList DB table Handler
    """

    @classmethod
    def new_todo_list_entry(cls, name: str) -> int:
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
    def get_lists_paginated(cls, page_number: int = 1, page_size: int = 10) -> List[TodoList]:
        """
        Return TodoLists entries from the DB paginated.

        The max `page_size` allowed is `MAX_PAGE_SIZE`,
         if a bigger value is received it will be set to `MAX_PAGE_SIZE`

        If a negative `page_number` is received it will be set to 1.

        :param page_number: Page number to return. Default 1
        :param page_size: Number of items per page. Default 10
        :return: TodoLists entries in that page
        """
        try:
            session = cls.session_maker()

            page_number = page_number if page_number > 0 else 1
            page_size = page_size if page_size < MAX_PAGE_SIZE else MAX_PAGE_SIZE

            _last_entry = page_number * page_size

            return session.query(TodoList).slice(_last_entry - page_size, _last_entry).all()
        finally:
            cls.session_maker.remove()

    @classmethod
    def get_todo_list(cls, list_id: int) -> TodoList:
        """
        Fetch a TodoList from the DB

        :param list_id: ID of list to fetch
        :return: TodoList
        :raise NoResultFound: If list with that ID does not exist
        """
        try:
            session = cls.session_maker()
            todo_list = session.query(TodoList).get(list_id)
            if not todo_list:
                print('TodoList with id "{}" does not exist'.format(list_id))
                raise NoResultFound()
            return todo_list
        finally:
            cls.session_maker.remove()

    @classmethod
    def delete_todo_list(cls, list_id: int) -> None:
        """
        Delete a TodoList from the DB

        :param list_id: ID of list to delete
        :return:
        :raise NoResultFound: If list with that ID does not exist
        """
        try:
            session = cls.session_maker()
            todo_list = session.query(TodoList).filter(TodoList.id == list_id).delete()
            if not todo_list:
                print('TodoList with id "{}" does not exist'.format(list_id))
                raise NoResultFound()
            session.commit()
        finally:
            cls.session_maker.remove()

    @classmethod
    def get_lists_db_count(cls) -> int:
        """
        :return: count of TodoLists in the DB
        """
        try:
            session = cls.session_maker()
            return session.query(TodoList).count()
        finally:
            cls.session_maker.remove()
