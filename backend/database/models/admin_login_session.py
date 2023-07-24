from datetime import datetime as dt

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from app_init import base
from .admin import AdminModel


class AdminLoginSessionModel(base):
    __tablename__ = 'admin_login_session'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    admin_id = Column(Integer, ForeignKey(AdminModel.id, ondelete='CASCADE'), index=True, nullable=False, )
    session_hash = Column(String(255), index=True, nullable=False, )
    end_date = Column(DateTime, nullable=False, default=dt.utcnow, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'session_hash': self.session_hash,
            'end_date': self.end_date,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(AdminLoginSessionModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs

    def __str__(self, ) -> str:
        return f'AdminId: {self.admin_id}\nSessionHash: {self.session_hash}\nEndDate: {self.end_date}\n'

    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array