from app_init import base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float


class ChannelReactionsModel(base):
    __tablename__ = 'channel_reactions'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    channel_id = Column(Integer, ForeignKey("channel.id", ondelete="CASCADE"), nullable=False, )
    emoji_type = Column(String(2), nullable=False, )
    subscribers_percent_from = Column(Float, default=0, nullable=False, )
    subscribers_percent_to = Column(Float, default=0, nullable=False, )

    def to_dict(self):
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "emoji_type": self.emoji_type,
            "subscribers_percent_from": self.subscribers_percent_from,
            "subscribers_percent_to": self.subscribers_percent_to
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

    def __str__(self, ) -> str:
        return f"ID: {self.id}\n" \
               f"Channel ID: {self.channel_id}\n" \
               f"Emoji: {self.emoji_type}\n" \
               f"Subscriber percent from: {self.subscribers_percent_from}\n" \
               f"Subscriber percent to: {self.subscribers_percent_to}"
