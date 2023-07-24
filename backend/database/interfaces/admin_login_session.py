from datetime import datetime as dt

from sqlalchemy.orm import Session

from app_init import engine
from database.models import AdminLoginSessionModel
from .admin import AdminInterface


class AdminLoginSessionInterface:
    @classmethod
    def create_model(cls, admin_login_session_model_admin_id: int, admin_login_session_model_session_hash: str,
                     admin_login_session_model_end_date: dt, ) -> int | bool:
        """Создание модели авторизации"""
        if not AdminInterface.check_is_exists(admin_login_session_model_admin_id):
            return False
        connection = engine()
        with Session(connection) as session:
            model = AdminLoginSessionModel(
                admin_id=admin_login_session_model_admin_id,
                session_hash=admin_login_session_model_session_hash,
                end_date=admin_login_session_model_end_date,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, admin_login_session_model_id: int) -> bool:
        """Проверка на существование модели авторизации по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.id == admin_login_session_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, admin_login_session_model_id: int, ) -> AdminLoginSessionModel:
        """Получение модели авторизации по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.id == admin_login_session_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, admin_login_session_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели авторизации по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.id == admin_login_session_model_id).update({setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, admin_login_session_model_id: int, ) -> bool:
        """Удаление модели авторизации по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.id == admin_login_session_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_admin_id(cls, admin_login_session_model_admin_id: int, ) -> AdminLoginSessionModel:
        """Получение модели авторизации по ID админа"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.admin_id == admin_login_session_model_admin_id).first()
        connection.dispose()
        return model

    @classmethod
    def get_first_by_session_hash(cls, admin_login_session_model_session_hash: str, ) -> AdminLoginSessionModel:
        """Получение модели авторизации по хэшу сессии"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AdminLoginSessionModel).filter(
                AdminLoginSessionModel.session_hash == admin_login_session_model_session_hash).first()
        connection.dispose()
        return model
