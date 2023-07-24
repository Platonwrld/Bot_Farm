from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy import inspect
from app_init import base


class UNameModel(base):
    __tablename__ = 'u_name'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    type = Column(String(20), index=True, nullable=False, )
    gender = Column(String(20), index=True, nullable=False, )
    value = Column(String(20), index=True, nullable=False, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'type': self.type,
            'gender': self.gender,
            'value': self.value,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(UNameModel).attrs
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
        return f'Type: {self.type}\nGender: {self.gender}\nValue: {self.value}\n'
