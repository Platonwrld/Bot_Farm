import json
import vk_api
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from telebot import TeleBot




def get_settings():
    """Функция получения конфигурации"""
    file = open(Path(Path.cwd(), 'config.json'), 'r')
    data = file.read()
    file.close()
    config = json.loads(data)
    return config


def engine():
    """Функция создания соединения с базой"""
    config = get_settings()
    engine = create_engine(
        f"mysql+pymysql://{config['mysql']['user']}:{config['mysql']['password']}@{config['mysql']['host']}/"
        f"{config['mysql']['database']}")
    return engine

def get_vk_api():
    """Функция подключения VK API"""
    config = get_settings()
    vk_session = vk_api.VkApi(config['vk_login'], config['vk_password'])
    vk_session.auth()
    return vk_session.get_api()

base = declarative_base()
config = get_settings()
tg_bot = TeleBot(config['tg_bot_api_key'])

#
if __name__ == "__main__":
    """Создание всех моделей БД"""
    from database.models import *

    for model in models:
        print(f"Create {model.__tablename__} table")
    base.metadata.create_all(engine())

flask_app = Flask(__name__)
CORS(flask_app)
