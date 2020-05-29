from database.database import Database
from database.tables.TodoLists import TodoList
from typing import Optional
from sqlalchemy.exc import IntegrityError


class TodoListDBHandler(Database):

    @classmethod
    def new_todo_list_entry(cls, name: str) -> Optional[int]:
        """
        Create a new todoList entry in the database

        :param name:
        :return: New todoList entry id
        """
        try:
            session = cls.session_maker()
            new_todo_list = TodoList(name=name)
            session.add(new_todo_list)
            session.commit()
            new_id = new_todo_list.id
            return new_id
        except IntegrityError as e:
            print('TodoList name must be unique. List with name "{}" already exist'.format(name))
            raise e
        finally:
            cls.session_maker.remove()

    @classmethod
    def get_all(cls):
        try:
            session = cls.session_maker()
            return session.query(TodoList).all()
        finally:
            cls.session_maker.remove()
