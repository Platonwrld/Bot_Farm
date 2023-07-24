from app_init import engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from database.models import BioModel


class BioInterface:
    @classmethod
    def create_bio(cls, bio_text: str, is_male: bool) -> int:
        """Создание модели биографии"""
        connection = engine()
        with Session(connection) as session:
            model = BioModel(
                bio_text=bio_text,
                is_male=is_male
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id


    @classmethod
    def check_bio_is_exists(cls, bio_text: str):
        """Проверка модели на существование"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(BioModel).filter(BioModel.bio_text == bio_text).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_random_bio(cls, is_male: bool) -> BioModel:
        """Получение случайной модели биографии"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(BioModel).filter(BioModel.is_male == is_male).order_by(func.rand()).first()
        connection.dispose()
        return model

    @classmethod
    def update_bio_by_id(cls, model_id: int, setting_name: str, setting_value: any) -> bool:
        """Обновление модели биографии"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(BioModel).filter(BioModel.id == model_id).update({
                setting_name: setting_value
            })
            session.commit()
        connection.dispose()
        return count > 0