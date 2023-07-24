from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from app_init import base
from .admin import AdminModel


class NicknameModel(base):
    __tablename__ = 'nickname'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    first_name = Column(String(255), nullable=False, )
    last_name = Column(String(255), )
    username = Column(String(255), )
    is_used = Column(Boolean, default=False, )
    is_male = Column(Boolean, default=False, )

    def to_dict(self, ) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "is_used": self.is_used
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