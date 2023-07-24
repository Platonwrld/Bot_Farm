from datetime import datetime as dt

from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime as dt

from app_init import engine
from database.models import TaskForMakeModel



class TaskForMakeInterface:
    @classmethod
    def create_model(cls, task_type: str, task_arguments: list | tuple, make_time: dt):
        connection = engine()
        with Session(connection) as session:
            model = TaskForMakeModel(
                task_type=task_type,
                task_arguments=task_arguments,
                make_time=make_time
            )
            session.add(model)
            session.commit()
            model_id = model.id
        connection.dispose()
        return model_id

    @classmethod
    def delete_model_by_id(cls, model_id: int):
        connection = engine()
        with Session(connection) as session:
            count = session.query(TaskForMakeModel).filter(TaskForMakeModel.id == model_id).delete()
            session.commit()
        connection.dispose()
        return count > 0

    @classmethod
    def get_must_make_tasks(cls, ) -> list[TaskForMakeModel]:
        connection = engine()
        with Session(connection) as session:
            models = session.query(TaskForMakeModel).filter(TaskForMakeModel.make_time < dt.utcnow()).all()
        connection.dispose()
        return models

