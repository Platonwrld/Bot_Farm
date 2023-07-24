from sqlalchemy.orm import Session

from app_init import engine
from database.models import TaskModel


class TaskInterface:
    @classmethod
    def create_model(cls, task_model_name: str, task_model_type: str, task_model_required_count: int, ) -> int:
        """Создание модели задачи"""
        connection = engine()
        with Session(connection) as session:
            model = TaskModel(
                name=task_model_name,
                type=task_model_type,
                required_count=task_model_required_count,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, task_model_id: int) -> bool:
        """Проверка на существование модели задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskModel).filter(TaskModel.id == task_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_count_by_(cls, ) -> int:
        """Получение количества всех задач"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskModel).filter().count()
        connection.dispose()
        return count

    @classmethod
    def get_first_by_id(cls, task_model_id: int, ) -> TaskModel:
        """Получение модели задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TaskModel).filter(TaskModel.id == task_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, task_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskModel).filter(TaskModel.id == task_model_id).update({setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, task_model_id: int, ) -> bool:
        """Удаление модели задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskModel).filter(TaskModel.id == task_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_pagination_by_(cls, limit: int, page: int, ) -> list[TaskModel]:
        """Пагинация всех моделей задач"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TaskModel).filter().limit(limit).offset((page - 1) * limit).all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by_(cls, ) -> list[TaskModel]:
        """Получение всех моделей задач"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TaskModel).filter().all()
        connection.dispose()
        return models

    @classmethod
    def get_all_by_task_type(cls, task_type: str) -> list[TaskModel]:
        """Получение всех задач по типу задачи"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TaskModel).filter(TaskModel.type == task_type).all()
        connection.dispose()
        return models
