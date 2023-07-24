from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base
from sqlalchemy import inspect


class TaskModel(base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    name = Column(String(255), index=True, nullable=False, )
    type = Column(String(255), index=True, nullable=False, )
    required_count = Column(Integer, nullable=False, )
    is_activate = Column(Boolean, default=False)

    def to_dict(self, ) -> dict:
        return {
            "id": self.id,
            'name': self.name,
            'type': self.type,
            'required_count': self.required_count,
            'is_activate': self.is_activate
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(TaskModel).attrs
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
        return f'Name: {self.name}\nType: {self.type}\nRequiredCount: {self.required_count}\n'
