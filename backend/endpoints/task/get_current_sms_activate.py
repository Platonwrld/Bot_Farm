from flask import Flask
from flask import request

from database.interfaces import TaskInterface
from app_init import get_settings

from decorators.flask import is_logged_in_flask_decorator


def add_task_get_current_sms_active(app: Flask):
    @app.route('/task/get_current_sms_active', methods=['POST'])
    @is_logged_in_flask_decorator
    def task_get_current_sms_active():
        return {'status': True, 'data': get_settings()['current_sms_activate_api_key']}
