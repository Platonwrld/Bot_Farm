from app_init import engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import and_
from database.models import AvatarModel


class AvatarInterface:
    @classmethod
    def create_avatar(cls, download_href: str, is_male: bool, ) -> int:
        """Создание нового авторизации"""
        connection = engine()
        with Session(connection) as session:
            model = AvatarModel(
                download_href=download_href,
                is_male=is_male
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists_by_download_href(cls, download_href: str):
        """Проверка модели на существование"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AvatarModel).filter(AvatarModel.download_href == download_href).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_random_avatar(cls, is_male: bool) -> AvatarModel:
        """Получение случайного аватара по полу"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(AvatarModel).filter(and_(AvatarModel.is_male==is_male)).order_by(func.rand()).first()
        connection.dispose()
        return model

    @classmethod
    def update_avatar_by_id(cls, model_id: int, setting_name: str, setting_value: any) -> bool:
        """Обновление аватара по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(AvatarModel).filter(AvatarModel.id == model_id).update({
                setting_name: setting_value
            })
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_all_by_has_not_path(cls, ) -> list[AvatarModel]:
        """Получение всех моделей без записанных файлов"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(AvatarModel).filter(AvatarModel.path_to_file == None).all()
        connection.dispose()
        return models