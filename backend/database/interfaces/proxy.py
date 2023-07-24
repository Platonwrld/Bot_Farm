from datetime import datetime as dt

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app_init import engine
from database.models import ProxyModel


class ProxyInterface:
    @classmethod
    def create_model(cls, proxy_model_type: str, proxy_model_ip: str, proxy_model_port: int,
                     proxy_model_username: str = None, proxy_model_password: str = None,
                     proxy_model_last_use: dt = None, proxy_model_is_active: bool = None, ) -> int:
        """Создание модели прокси"""
        connection = engine()
        with Session(connection) as session:
            model = ProxyModel(
                type=proxy_model_type,
                ip=proxy_model_ip,
                port=proxy_model_port,
                username=proxy_model_username,
                password=proxy_model_password,
                last_use=proxy_model_last_use,
                is_active=proxy_model_is_active,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, proxy_model_id: int) -> bool:
        """Проверка модели прокси на существование"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ProxyModel).filter(ProxyModel.id == proxy_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, proxy_model_id: int, ) -> ProxyModel:
        """Получение модели прокси по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ProxyModel).filter(ProxyModel.id == proxy_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def get_first_by_ip(cls, proxy_model_ip: str, ) -> ProxyModel:
        """Получение модели прокси по IP"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ProxyModel).filter(ProxyModel.ip == proxy_model_ip).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, proxy_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обнолвение модели прокси по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ProxyModel).filter(ProxyModel.id == proxy_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, proxy_model_id: int, ) -> bool:
        """Удаление модели прокси по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ProxyModel).filter(ProxyModel.id == proxy_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_count_by_(cls, ):
        """Получение количества всех прокси"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(ProxyModel).filter().count()
        connection.dispose()
        return count

    @classmethod
    def get_pagination_by_(cls, limit: int, page: int, ) -> list[ProxyModel]:
        """Пагинация всех моделей прокси"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(ProxyModel).filter().limit(limit).offset((page - 1) * limit).all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by(cls, ) -> list[ProxyModel]:
        """Получение всех моделей прокси"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(ProxyModel).filter().all()
        connection.dispose()
        return models

    @classmethod
    def get_random_active_proxy(cls, ) -> ProxyModel:
        """Получение случайной модели прокси"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(ProxyModel).filter(ProxyModel.is_active == True).order_by(func.random()).first()
        connection.dispose()
        return model
