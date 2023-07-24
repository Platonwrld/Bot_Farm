from sqlalchemy.orm import Session

from app_init import engine
from database.models import ChannelReactionsModel
from sqlalchemy import and_


class ChannelReactionsInterface:
    @classmethod
    def create_model(cls, channel_id: int, emoji_type: str):
        """Создание модели процентов реакциий канала"""
        connection = engine()
        with Session(connection) as session:
            model = ChannelReactionsModel(
                channel_id=channel_id,
                emoji_type=emoji_type
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def update_model_by_id(cls, model_id: int, setting_name: str,
                                                  setting_value: any):
        """Обновление модели по типу реакции и ID канала"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ChannelReactionsModel).filter(ChannelReactionsModel.id == model_id).update({
                setting_name: setting_value
            })
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_channel_emojis(cls, channel_id: int) -> list[ChannelReactionsModel]:
        """Получение всех моделей каналов по ID канала"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(ChannelReactionsModel).filter(ChannelReactionsModel.channel_id == channel_id).all()
        connection.dispose()
        return models
