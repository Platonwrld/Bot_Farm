from datetime import datetime as dt
from datetime import timedelta as td

from sqlalchemy.orm import Session

from app_init import engine
from database.models import TgClientModel

from sqlalchemy import and_


class TgClientInterface:
    @classmethod
    def create_model(cls, tg_client_model_client_hash: str, tg_client_model_phone_number: str,
                     tg_client_model_tg_app_id: int, tg_client_model_device_id: int, tg_client_model_u_fname_id: int,
                     tg_client_model_u_lname_id: int, tg_client_model_u_sname_id: int, tg_client_model_username: str,
                     tg_client_model_is_ban: bool, tg_client_model_proxy_id: int, ) -> int | bool:
        """Создание модели Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            model = TgClientModel(
                client_hash=tg_client_model_client_hash,
                phone_number=tg_client_model_phone_number,
                tg_app_id=tg_client_model_tg_app_id,
                device_id=tg_client_model_device_id,
                proxy_id=tg_client_model_proxy_id,
                u_fname_id=tg_client_model_u_fname_id,
                u_lname_id=tg_client_model_u_lname_id,
                u_sname_id=tg_client_model_u_sname_id,
                username=tg_client_model_username,
                is_ban=tg_client_model_is_ban,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, tg_client_model_id: int) -> bool:
        """Проверка наличие модели Telegram клиента"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.id == tg_client_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, tg_client_model_id: int, ) -> TgClientModel:
        """Получение модели Telegram клиента по iD"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TgClientModel).filter(TgClientModel.id == tg_client_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, tg_client_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обнолвение модели Telegram клиента по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.id == tg_client_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, tg_client_model_id: int, ) -> bool:
        """Удаление модели Telegram клиента по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.id == tg_client_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_phone_number(cls, tg_client_model_phone_number: str, ) -> TgClientModel:
        """Получение модели Telegram клиента по номеру телефона"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TgClientModel).filter(
                TgClientModel.phone_number == tg_client_model_phone_number).first()
        connection.dispose()
        return model

    @classmethod
    def get_count_by_(cls, ) -> int:
        """Получение количества Telegram клиентов"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter().count()
        connection.dispose()
        return count

    @classmethod
    def get_count_by_is_banned(cls, is_banned: bool) -> list[TgClientModel]:
        """Получение количества заблокированных / незаблокированных Telegram клиентов"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.is_ban == is_banned).count()
        connection.dispose()
        return count

    @classmethod
    def get_count_by_creation_time_less(cls, less_creation_time: dt) -> list[TgClientModel]:
        """Получение количества Telegram клиентов позже определенного времени"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.creation_time > less_creation_time).count()
        connection.dispose()
        return count

    @classmethod
    def get_count_by_proxy(cls, proxy_id: int) -> int:
        """Получение количества Telegram клиентов по ID прокси"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgClientModel).filter(TgClientModel.proxy_id == proxy_id).count()
        connection.dispose()
        return count

    @classmethod
    def get_pagination_by_(cls, limit: int, page: int, ) -> list[TgClientModel]:
        """Пагинация Telegram клиентов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgClientModel).filter().limit(limit).offset((page - 1) * limit).all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by_proxy_id(cls, proxy_id: int) -> list[TgClientModel]:
        """Получение всех Telegram клиентов по ID прокси"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgClientModel).filter(TgClientModel.proxy_id == proxy_id).all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by_(cls) -> list[TgClientModel]:
        """Получение всех Telegram клиентов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgClientModel).filter().all()
        connection.dispose()
        return models

    @classmethod
    def get_all_not_banned(cls) -> list[TgClientModel]:
        """Получение всех незаблокированных Telegram клиентов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgClientModel).filter(and_(
                    TgClientModel.is_ban == False,
                    TgClientModel.creation_time < dt.utcnow() - td(days=7)
            )).all()
        connection.dispose()
        return models
