import json
from datetime import datetime as dt
from datetime import timedelta as td

from flask import Flask

from database.interfaces import ChannelInterface
from database.interfaces import ProxyInterface
from database.interfaces import TaskInterface
from database.interfaces import TaskMakeInterface
from database.interfaces import TgClientInterface
from app_init import get_settings
from pathlib import Path

from decorators.flask import is_logged_in_flask_decorator


def add_set_is_null_notificated(app: Flask):
    @app.route("/set_is_null_notificated", methods=['POST'])
    @is_logged_in_flask_decorator
    def set_is_null_notificated():
        config = get_settings()
        config.update({
            "is_null_notificated": not config['is_null_notificated']
        })
        with open(Path(Path.cwd(), 'config.json'), 'w') as file:
            json.dump(config, file, indent=4)
        return {
            "status": True,
            "data": config['is_null_notificated']
        }
