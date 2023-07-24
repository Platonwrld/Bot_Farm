from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from app_init import base
from .admin import AdminModel


class BioModel(base):
    __tablename__ = 'bio'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    bio_text = Column(String(150), nullable=False, )
    is_male = Column(Boolean, nullable=False, )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bio_text": self.bio_text
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
