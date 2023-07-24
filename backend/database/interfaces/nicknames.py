from app_init import engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from database.models import NicknameModel


class NicknameInterface:
    @classmethod
    def create_nickname(cls, first_name: str, last_name: str, username: str, is_male: bool) -> int:
        """Создание модели никнейма"""
        connection = engine()
        with Session(connection) as session:
            model = NicknameModel(
                first_name=first_name,
                last_name=last_name,
                username=username,
                is_male=is_male,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_model_is_exists(cls, first_name: str, last_name: str, username: str):
        """Проверка модели на существование"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(NicknameModel).filter(and_(
                NicknameModel.first_name==first_name,
                NicknameModel.last_name==last_name,
                NicknameModel.username==username
            )).count()
        return count > 0

    @classmethod
    def get_random_nickname(cls, is_male: bool) -> NicknameModel:
        """Получение случайного никнейма"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(NicknameModel).filter(and_(NicknameModel.is_used==False, NicknameModel.is_male==is_male)).order_by(func.rand()).first()
        connection.dispose()
        return model

    @classmethod
    def update_nickname_by_id(cls, model_id: int, setting_name: str, setting_value: any) -> bool:
        """Обновление никнейма по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(NicknameModel).filter(NicknameModel.id == model_id).update({
                setting_name: setting_value
            })
            session.commit()
        connection.dispose()
        return count > 0
