from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from sqlalchemy import Float

from app_init import base


class ChannelModel(base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    channel_id = Column(BigInteger, index=True, nullable=False, )
    channel_name = Column(String(255), index=True, nullable=False, )
    channel_invite_link = Column(String(255), index=True, nullable=False, )
    is_seen_active = Column(Boolean, index=True, nullable=False, )
    view_percent_from = Column(Float, nullable=False, default=0, )
    view_percent_to = Column(Float, nullable=False, default=0, )

    def to_dict(self, ) -> dict:
        return {
            "id": self.id,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'channel_invite_link': self.channel_invite_link,
            'is_seen_active': self.is_seen_active,
            'view_percent_from': self.view_percent_from,
            'view_percent_to': self.view_percent_to
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(ChannelModel).attrs
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
        return f'ChannelId: {self.channel_id}\nChannelName: {self.channel_name}\nChannelInviteLink: {self.channel_invite_link}\nIsSeenActive: {self.is_seen_active}\n'
