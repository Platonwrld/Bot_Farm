from sqlalchemy.orm import Session

from app_init import engine
from database.models import TaskArgumentModel
from .task import TaskInterface


class TaskArgumentInterface:
    @classmethod
    def create_model(cls, task_argument_model_task_id: int, task_argument_model_name: str,
                     task_argument_model_value: str, ) -> int | bool:
        """Создание модели аргумента задачи"""
        if not TaskInterface.check_is_exists(task_argument_model_task_id):
            return False
        connection = engine()
        with Session(connection) as session:
            model = TaskArgumentModel(
                task_id=task_argument_model_task_id,
                name=task_argument_model_name,
                value=task_argument_model_value,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, task_argument_model_id: int) -> bool:
        """Проверка на существование модели аргумента задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskArgumentModel).filter(TaskArgumentModel.id == task_argument_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, task_argument_model_id: int, ) -> TaskArgumentModel:
        """Получение модели аргумента задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TaskArgumentModel).filter(TaskArgumentModel.id == task_argument_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, task_argument_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обнолвение модели аргумента задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskArgumentModel).filter(TaskArgumentModel.id == task_argument_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, task_argument_model_id: int, ) -> bool:
        """Удаление модели аргумента задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskArgumentModel).filter(TaskArgumentModel.id == task_argument_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_all_by_task_id(cls, task_argument_model_task_id: int, ) -> list[TaskArgumentModel]:
        """Получение всех моделей аргументов задачи по ID задачи"""
        connection = engine()
        with Session(connection) as session:
            models = session.query(TaskArgumentModel).filter(
                TaskArgumentModel.task_id == task_argument_model_task_id).all()
        connection.dispose()
        return models
