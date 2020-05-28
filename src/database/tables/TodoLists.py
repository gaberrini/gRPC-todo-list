import database.database as db
from sqlalchemy import Column, Integer, String


class TodoList(db.Base):
    __tablename__ = 'todo-lists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
