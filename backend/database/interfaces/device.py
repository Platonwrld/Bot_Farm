from sqlalchemy import func
from sqlalchemy.orm import Session

from app_init import engine
from database.models import DeviceModel


class DeviceInterface:
    @classmethod
    def create_model(cls, device_model_os: str, device_model_device_model: str,
                     device_model_system_version: str, ) -> int:
        """Создание модели устройства"""
        connection = engine()
        with Session(connection) as session:
            model = DeviceModel(
                os=device_model_os,
                device_model=device_model_device_model,
                system_version=device_model_system_version,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, device_model_id: int) -> bool:
        """Проверка модели устройства по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(DeviceModel).filter(DeviceModel.id == device_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, device_model_id: int, ) -> DeviceModel:
        """Получение модели устройства по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(DeviceModel).filter(DeviceModel.id == device_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, device_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели устройства по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(DeviceModel).filter(DeviceModel.id == device_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, device_model_id: int, ) -> bool:
        """Удаление модели устройства по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(DeviceModel).filter(DeviceModel.id == device_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_pagination_by_os(cls, device_model_os: str, limit: int, page: int, ) -> list[DeviceModel]:
        """Пагинация моделей устройств по операционной системе"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(DeviceModel).filter(DeviceModel.os == device_model_os).limit(limit).offset(
                (page - 1) * limit).all()
        connection.dispose()
        return models

    @classmethod
    def get_rand_(cls) -> DeviceModel:
        """Получение случайного устройства по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(DeviceModel).filter().order_by(func.rand()).first()
        connection.dispose()
        return model
