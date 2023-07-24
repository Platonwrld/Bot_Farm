from sqlalchemy import BINARY
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from app_init import base


class AdminModel(base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    username = Column(String(255), index=True, nullable=False, )
    password = Column(BINARY(60), nullable=False, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(AdminModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs

    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array

    def __str__(self, ) -> str:
        return f'Username: {self.username}\nPassword: {self.password}\n'
