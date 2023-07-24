from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect

from app_init import base
from .task import TaskModel


class TaskArgumentModel(base):
    __tablename__ = 'task_argument'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    task_id = Column(Integer, ForeignKey(TaskModel.id, ondelete='CASCADE'), nullable=False, )
    name = Column(String(255), index=True, nullable=False, )
    value = Column(String(255), index=True, nullable=False, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'task_id': self.task_id,
            'name': self.name,
            'value': self.value,
        }
    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array

    @classmethod
    def get_columns(cls):
        attrs = inspect(TaskArgumentModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs

    def __str__(self, ) -> str:
        return f'TaskId: {self.task_id}\nName: {self.name}\nValue: {self.value}\n'
