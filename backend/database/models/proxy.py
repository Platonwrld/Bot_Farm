from datetime import datetime as dt

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base
from sqlalchemy import inspect


class ProxyModel(base):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    type = Column(String(20), index=True, nullable=False, )
    ip = Column(String(60), nullable=False, )
    port = Column(Integer, nullable=False, )
    username = Column(String(255), )
    password = Column(String(255), )
    last_use = Column(DateTime, index=True, default=dt.utcnow, )
    is_active = Column(Boolean, index=True, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'type': self.type,
            'ip': self.ip,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'last_use': self.last_use,
            'is_active': self.is_active,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(ProxyModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs

    def __str__(self, ) -> str:
        return f'Type: {self.type}\nIp: {self.ip}\nPort: {self.port}\nUsername: {self.username}\nPassword: {self.password}\nLastUse: {self.last_use}\nIsActive: {self.is_active}\n'

    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array