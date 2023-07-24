from datetime import datetime as dt

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app_init import engine
from database.models import TaskMakeModel
from .task import TaskInterface
from .tg_client import TgClientInterface


class TaskMakeInterface:
    @classmethod
    def create_model(cls, task_make_model_task_id: int, task_make_model_from_account: int,
                     task_make_model_status: bool, ) -> int | bool:
        """Создание модели отчета о выполнении задачи"""
        if not TaskInterface.check_is_exists(task_make_model_task_id):
            return False
        if not TgClientInterface.check_is_exists(task_make_model_from_account):
            return False
        connection = engine()
        with Session(connection) as session:
            model = TaskMakeModel(
                task_id=task_make_model_task_id,
                from_account=task_make_model_from_account,
                status=task_make_model_status,
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def check_is_exists(cls, task_make_model_id: int) -> bool:
        """Проверка модели отчета о выполнении задачи на существование"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter(TaskMakeModel.id == task_make_model_id).count()
        connection.dispose()
        return count > 0

    @classmethod
    def get_first_by_id(cls, task_make_model_id: int, ) -> TaskMakeModel:
        """Получение модели отчета о выполнении задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            model = session.query(TaskMakeModel).filter(TaskMakeModel.id == task_make_model_id).first()
        connection.dispose()
        return model

    @classmethod
    def update_model_by_id(cls, task_make_model_id: int, setting_name: str, setting_value: any, ) -> bool:
        """Обновление модели отчета о выполнении задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter(TaskMakeModel.id == task_make_model_id).update(
                {setting_name: setting_value})
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def delete_model_by_id(cls, task_make_model_id: int, ) -> bool:
        """Удаление модели отчета о выполнении задачи по ID"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter(TaskMakeModel.id == task_make_model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_count_by_task_id_and_status(cls, task_make_model_status: bool, task_make_model_task_id: int, ) -> int:
        """Получение количества отчетов о выполнении задач по ID задачи и статусу выполнения"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter(and_(
                TaskMakeModel.task_id == task_make_model_task_id,
                TaskMakeModel.status == task_make_model_status)).count()
        connection.dispose()
        return count

    @classmethod
    def get_count_by(cls):
        """Получение количества всех выполнений задач"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter().count()
        connection.dispose()
        return count

    @classmethod
    def get_count_by_time_less(cls, less_time_date: dt):
        """Получение количества выполнений задач позже чем указаная дата"""
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskMakeModel).filter(TaskMakeModel.make_time > less_time_date).count()
        connection.dispose()
        return count
