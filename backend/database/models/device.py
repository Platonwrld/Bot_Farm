from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect

from app_init import base


class DeviceModel(base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, )
    os = Column(String(20), index=True, nullable=False, )
    device_model = Column(String(255), nullable=False, )
    system_version = Column(String(255), nullable=False, )

    def to_dict(self, ) -> dict:
        return {
            'id': self.id,
            'os': self.os,
            'device_model': self.device_model,
            'system_version': self.system_version,
        }

    @classmethod
    def get_columns(cls):
        attrs = inspect(DeviceModel).attrs
        ignore_attrs = []
        for ignore_attr in ignore_attrs:
            attrs.pop(ignore_attr)
        return ignore_attrs

    def __str__(self, ) -> str:
        return f'Os: {self.os}\nDeviceModel: {self.device_model}\nSystemVersion: {self.system_version}\n'

    def to_array(self) -> list:
        array = []
        data = self.to_dict()
        for key in data:
            if type(data[key]) == bool:
                array.append(data[key])
            else:
                array.append(str(data[key]))
        return array
