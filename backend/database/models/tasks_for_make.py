from datetime import datetime as dt

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer

from app_init import base




class TaskForMakeModel(base):
    __tablename__ = 'task_for_make'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    task_type = Column(String(255), nullable=False, )
    task_arguments = Column(JSON, nullable=False, )
    make_time = Column(DateTime, nullable=False, )



    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "task_arguments": self.task_arguments,
            "make_time": self.make_time
        }

    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array