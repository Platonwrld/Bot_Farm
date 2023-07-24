from bcrypt import checkpw
from bcrypt import gensalt
from bcrypt import hashpw
from sqlalchemy.orm import Session

from app_init import engine
from database.models import AdminModel


class AdminInterface:
    @classmethod
    def create_model(cls, admin_model_username: str, admin_model_password: str, ) -> int:
        """Создание модели администратора"""
        admin_model_password = hashpw(admin_model_password.encode('utf-8'), gensalt())
        connection = engine()
        with Session(connection) as session:
            model = AdminModel(
                username=admin_model_username,
                password=admin_model_password,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, admin_model_id: int) -> bool:
        """Проверка на существование модели администратора"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminModel).filter(AdminModel.id == admin_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, admin_model_id: int, ) -> AdminModel:
        """Получение модели администратора по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AdminModel).filter(AdminModel.id == admin_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, admin_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели администратора по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminModel).filter(AdminModel.id == admin_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, admin_model_id: int, ) -> bool:
        """Удаление модели администратора по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AdminModel).filter(AdminModel.id == admin_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def check_password(cls, admin_model_id: int, admin_model_password: str) -> bool:
        """Проверка пароля администратора по ID"""
        model = AdminInterface.get_first_by_id(admin_model_id)
        if model:
            return checkpw(admin_model_password.encode('utf-8'), model.password)
        return False

    @classmethod
    def update_password(cls, admin_model_id: int, admin_model_password: str) -> bool:
        """Обновление пароля администратора"""
        admin_model_password = hashpw(admin_model_password.encode('utf-8'), gensalt())
        return AdminInterface.update_model_by_id(admin_model_id, 'password', admin_model_password)

    @classmethod
    def get_first_by_username(cls, admin_model_username: str, ) -> AdminModel:
        """Получение модели администратора по имени пользователя"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AdminModel).filter(AdminModel.username == admin_model_username).first()
        connection.dispose()
        return model
