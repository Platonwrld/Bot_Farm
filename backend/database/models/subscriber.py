from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app_init import base
from .channel import ChannelModel
from .tg_client import TgClientModel
from sqlalchemy import inspect


class SubscriberModel(base):
    __tablename__ = "subscriber"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    channel_id = Column(Integer, ForeignKey(ChannelModel.id, ondelete="CASCADE"), nullable=False, )
    tg_client_id = Column(Integer, ForeignKey(TgClientModel.id, ondelete="CASCADE"), nullable=False, )
    active_view = Column(Boolean, nullable=False, )


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'tg_client_id': self.tg_client_id,
            "active_view": self.active_view
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(SubscriberModel).attrs
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