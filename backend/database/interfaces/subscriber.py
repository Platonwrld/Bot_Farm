from sqlalchemy import and_
from sqlalchemy.orm import Session

from app_init import engine
from database.models import SubscriberModel


class SubscriberInterface:
    @classmethod
    def create_subscriber(cls, channel_id: int, tg_client_id: int, active_view: bool):
        """Создание модели подписку"""
        connection = engine()
        with Session(connection) as session:
            model = SubscriberModel(
                channel_id=channel_id,
                tg_client_id=tg_client_id,
                active_view=active_view,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def get_all_by_channel_id(cls, channel_id: int, ) -> list[SubscriberModel]:
        """Получение всех моделей подписок по ID канала"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(SubscriberModel).filter(SubscriberModel.channel_id == channel_id).all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by_tg_client_id(cls, tg_client_id: int, ):
        """Получение всех подписок по ID Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(SubscriberModel).filter(SubscriberModel.tg_client_id == tg_client_id).all()
        connection.dispose()
        return models

    @classmethod
    def check_user_is_subscriber(cls, channel_id: int, tg_client_id: int):
        """Проверка пользователя на наличие подписки по ID Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(SubscriberModel).filter(and_(SubscriberModel.tg_client_id == tg_client_id,
                                                               SubscriberModel.channel_id == channel_id)).count()
        connection.dispose()
        return count > 0


    @classmethod
    def delete_by_model_id(cls, channel_id: int, tg_client_id: int):
        """Удаление модели подписки по ID канала и Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(SubscriberModel).filter(and_(
                SubscriberModel.channel_id == channel_id,
                SubscriberModel.tg_client_id == tg_client_id,
            )).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def check_is_exists_by_model_id(cls, channel_id: int, tg_client_id: int) -> bool:
        """Проверка модели подписки по ID канала и Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(SubscriberModel).filter(and_(
                SubscriberModel.channel_id == channel_id,
                SubscriberModel.tg_client_id == tg_client_id,
            )).count()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_count_by_channel_id(cls, channel_id: int):
        """Получение количества моделей подписок по ID канала"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(SubscriberModel).filter(SubscriberModel.channel_id == channel_id).count()
        connection.dispose()
        return count
