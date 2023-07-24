from datetime import datetime as dt

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base
from .device import DeviceModel
from .proxy import ProxyModel
from .tg_app import TgAppModel
from .u_name import UNameModel
from sqlalchemy import inspect


class TgClientModel(base):
    __tablename__ = 'tg_client'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    client_hash = Column(String(500), index=True, nullable=False, )
    phone_number = Column(String(30), index=True, nullable=False, )
    tg_app_id = Column(Integer, ForeignKey(TgAppModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    device_id = Column(Integer, ForeignKey(DeviceModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    proxy_id = Column(Integer, ForeignKey(ProxyModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    u_fname_id = Column(Integer, ForeignKey(UNameModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    u_lname_id = Column(Integer, ForeignKey(UNameModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    u_sname_id = Column(Integer, ForeignKey(UNameModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    username = Column(String(30), index=True, nullable=False, )
    is_spam = Column(Boolean, nullable=False, default=False, )
    is_ban = Column(Boolean, nullable=False, default=False, )
    creation_time = Column(DateTime, nullable=False, default=dt.utcnow)
    is_avatar_updated = Column(Boolean, default=False, )
    is_nickname_and_bio_updated = Column(Boolean, default=False, )

    def to_dict(self, ) -> dict:
        return {
            "id": self.id,
            "client_hash": self.client_hash,
            'phone_number': self.phone_number,
            'tg_app_id': self.tg_app_id,
            'device_id': self.device_id,
            'proxy_id': self.proxy_id,
            'u_fname_id': self.u_fname_id,
            'u_lname_id': self.u_lname_id,
            'u_sname_id': self.u_sname_id,
            'username': self.username,
            "is_spam": self.is_spam,
            'is_ban': self.is_ban,
            'creation_time': self.creation_time,
            "is_avatar_updated": self.is_avatar_updated,
            "is_nickname_and_bio_updated": self.is_nickname_and_bio_updated
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(TgClientModel).attrs
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
        return f'ClientHash: {self.client_hash}\nPhoneNumber: {self.phone_number}\nTgAppId: {self.tg_app_id}\nDeviceId: {self.device_id}\nUFnameId: {self.u_fname_id}\nULnameId: {self.u_lname_id}\nUSnameId: {self.u_sname_id}\nUsername: {self.username}\nIsBan: {self.is_ban}\n'
