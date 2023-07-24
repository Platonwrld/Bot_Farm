from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import Session

from app_init import engine
from database.models import UNameModel


class UNameInterface:
    @classmethod
    def create_model(cls, u_name_model_type: str, u_name_model_gender: str, u_name_model_value: str, ) -> int:
        """Создание модели имени / фамилиии / отчества"""
        connection = engine()
        with Session(connection) as session:
            model = UNameModel(
                type=u_name_model_type,
                gender=u_name_model_gender,
                value=u_name_model_value,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, u_name_model_id: int) -> bool:
        """Проверка на существование модели имени / фамилиии / отчества"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(UNameModel).filter(UNameModel.id == u_name_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, u_name_model_id: int, ) -> UNameModel:
        """Получение модели имени / фамилиии / отчества по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(UNameModel).filter(UNameModel.id == u_name_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, u_name_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели имени / фамилиии / отчества по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(UNameModel).filter(UNameModel.id == u_name_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, u_name_model_id: int, ) -> bool:
        """Удаление модели имени / фамилиии / отчества по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(UNameModel).filter(UNameModel.id == u_name_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_all_by_type_and_gender(cls, u_name_model_type: str, u_name_model_gender: str, ) -> list[UNameModel]:
        """Получение всех моделей имени / фамилиии / отчества по типу и полу"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(UNameModel).filter(and_(
                UNameModel.type == u_name_model_type, UNameModel.gender == u_name_model_gender)).all()
        connection.dispose()
        return models

    @classmethod
    def get_rand_by_type_and_gender(cls, type: str, gender: str):
        """Получение случайной модели имени / фамилиии / отчества по типу и полу"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(UNameModel).filter(
                and_(
                    UNameModel.gender == gender,
                    UNameModel.type == type
                )
            ).order_by(func.rand()).first()
        connection.dispose()
        return model
