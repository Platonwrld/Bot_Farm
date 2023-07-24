from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from sqlalchemy import Boolean
from app_init import base
from .admin import AdminModel


class AvatarModel(base):
    __tablename__ = 'avatar'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    download_href = Column(String(255), nullable=False, )
    path_to_file = Column(String(255), )
    is_male = Column(Boolean, )

    def to_dict(self):
        return {
            "id": self.id,
            "download_href": self.download_href,
            "path_to_file": self.path_to_file
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
