from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base
from sqlalchemy import inspect


class TgAppModel(base):
    __tablename__ = 'tg_app'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    os = Column(String(20), index=True, nullable=False, )
    app_id = Column(Integer, nullable=False, )
    app_hash = Column(String(255), nullable=False, )
    app_version = Column(String(255), index=True, nullable=False, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'os': self.os,
            'app_id': self.app_id,
            'app_hash': self.app_hash,
            'app_version': self.app_version,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(TgAppModel).attrs
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
        return f'Os: {self.os}\nAppId: {self.app_id}\nAppHash: {self.app_hash}\nAppVersion: {self.app_version}\n'
