from sqlalchemy.orm import Session

from app_init import engine
from database.models import ChannelModel
from .channel_reactions import ChannelReactionsInterface
from app_init import get_settings


class ChannelInterface:
    @classmethod
    def create_model(cls, channel_model_channel_id: int, channel_model_channel_name: str,
                     channel_model_channel_invite_link: str, channel_model_is_seen_active: bool, ) -> int:
        """Создание модели канала"""
        connection = engine()
        with Session(connection) as session:
            model = ChannelModel(
                channel_id=channel_model_channel_id,
                channel_name=channel_model_channel_name,
                channel_invite_link=channel_model_channel_invite_link,
                is_seen_active=channel_model_is_seen_active,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        config = get_settings()
        for emoji in config['default_emojis']:
            ChannelReactionsInterface.create_model(model_id, emoji)
        return model_id

    @classmethod
    def check_is_exists(cls, channel_model_id: int) -> bool:
        """Проверка модели канала на существование по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ChannelModel).filter(ChannelModel.id == channel_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, channel_model_id: int, ) -> ChannelModel:
        """Получение модели канала по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ChannelModel).filter(ChannelModel.id == channel_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, channel_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели канала по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ChannelModel).filter(ChannelModel.id == channel_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, channel_model_id: int, ) -> bool:
        """Удаление модели канала по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ChannelModel).filter(ChannelModel.id == channel_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_channel_id(cls, channel_model_channel_id: int, ) -> ChannelModel:
        """Получение модели канала по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ChannelModel).filter(ChannelModel.channel_id == channel_model_channel_id).first()
        connection.dispose()
        return model

    @classmethod
    def get_first_by_channel_invite_link(cls, channel_model_channel_invite_link: str, ) -> ChannelModel:
        """Получение модели канала по ссылке"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ChannelModel).filter(
                ChannelModel.channel_invite_link == channel_model_channel_invite_link).first()
        connection.dispose()
        return model


    @classmethod
    def get_all_by_(cls, ) -> list[ChannelModel]:
        """Получение всех моделей каналов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(ChannelModel).filter().all()
        connection.dispose()
        return models

    @classmethod
    def get_count_by_(cls, ) -> list[ChannelModel]:
        """Получение количества моделей каналов"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ChannelModel).filter().count()
        connection.dispose()
        return count

    @classmethod
    def get_pagination_by_(cls, limit: int, page: int, ) -> list[ChannelModel]:
        """Пагинация всех моделей каналов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(ChannelModel).filter().limit(limit).offset((page - 1) * limit).all()
        connection.dispose()
        return models
