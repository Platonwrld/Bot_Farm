from datetime import datetime as dt

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app_init import base
from .task import TaskModel
from .tg_client import TgClientModel
from sqlalchemy import inspect


class TaskMakeModel(base):
    __tablename__ = 'task_make'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    task_id = Column(Integer, ForeignKey(TaskModel.id, ondelete='CASCADE'), nullable=False, )
    from_account = Column(Integer, ForeignKey(TgClientModel.id, ondelete='CASCADE'), nullable=False, )
    status = Column(Boolean, nullable=False, )
    make_time = Column(DateTime, nullable=False, default=dt.utcnow, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'task_id': self.task_id,
            'from_account': self.from_account,
            'status': self.status,
            'make_time': self.make_time,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(TaskMakeModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs


    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array

    def __str__(self, ) -> str:
        return f'TaskId: {self.task_id}\nFromAccount: {self.from_account}\nStatus: {self.status}\nMakeTime: {self.make_time}\n'
