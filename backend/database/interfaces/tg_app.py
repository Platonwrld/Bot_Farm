from sqlalchemy import func
from sqlalchemy.orm import Session

from app_init import engine
from database.models import TgAppModel


class TgAppInterface:
    @classmethod
    def create_model(cls, tg_app_model_os: str, tg_app_model_app_id: int, tg_app_model_app_hash: str,
                     tg_app_model_app_version: str, ) -> int:
        """Создание модели TgAPP"""
        connection = engine()
        with Session(connection) as session:
            model = TgAppModel(
                os=tg_app_model_os,
                app_id=tg_app_model_app_id,
                app_hash=tg_app_model_app_hash,
                app_version=tg_app_model_app_version,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, tg_app_model_id: int) -> bool:
        """Проверка на существование данного TgAPP"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgAppModel).filter(TgAppModel.id == tg_app_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, tg_app_model_id: int, ) -> TgAppModel:
        """Получение модели TgAPP по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TgAppModel).filter(TgAppModel.id == tg_app_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, tg_app_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обнолвение модели TgAPP по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgAppModel).filter(TgAppModel.id == tg_app_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, tg_app_model_id: int, ) -> bool:
        """Удаление модели TgAPP по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TgAppModel).filter(TgAppModel.id == tg_app_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_all_by_(cls, ) -> list[TgAppModel]:
        """Получение всех моделей TgAPP"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgAppModel).filter().all()
        connection.dispose()
        return models

    @classmethod
    def get_rand_(cls) -> TgAppModel:
        """Получение случайного TgAPP"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TgAppModel).filter().order_by(func.rand()).first()
        connection.dispose()
        return models
