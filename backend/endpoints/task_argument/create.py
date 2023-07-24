import json
from datetime import datetime as dt

from flask import Flask
from flask import request

from database.interfaces import TaskArgumentInterface

from decorators.flask import is_logged_in_flask_decorator

from app_init import get_settings


def add_0(string: str):
    if len(string) == 1:
        return f"0{string}"
    return string


def add_create(app: Flask):
    @app.route('/task_argument/create', methods=['POST'])
    @is_logged_in_flask_decorator
    def task_argument_create():
        form_data = request.form
        if not form_data.get('task_argument_model_name') or not form_data.get(
                'task_argument_model_value') or not form_data.get('task_argument_model_task_id'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        task_argument_model_name = form_data.get('task_argument_model_name')
        task_argument_model_value = form_data.get('task_argument_model_value')
        task_argument_model_task_id = form_data.get('task_argument_model_task_id')
        if "start_t" in task_argument_model_name or "end_t" in task_argument_model_name:
            if task_argument_model_name == "start_t":
                task_argument_model_name = "start_time"
            else:
                task_argument_model_name = "end_time"
            tmp_date, tmp_time = task_argument_model_value.split(" ")
            dt_str = ""
            for tmp_d_v in tmp_date.split("-"):
                dt_str += add_0(tmp_d_v) + "-"
            dt_str = dt_str[:dt_str.rfind("-")]
            dt_str += " "
            for tmp_t_v in tmp_time.split(":"):
                dt_str += add_0(tmp_t_v)
                dt_str += ":"
            dt_str = dt_str[:dt_str.rfind(":")]
            task_argument_model_value = dt.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        create_task_argument_data = TaskArgumentInterface.create_model(
            task_argument_model_task_id=task_argument_model_task_id,
            task_argument_model_name=task_argument_model_name,
            task_argument_model_value=task_argument_model_value, )
        if task_argument_model_name == "sms_activate_api_key":
            settings = get_settings()
            settings.update({
                "current_sms_activate_api_key": task_argument_model_value
            })
            with open("config.json", 'w') as file:
                json.dump(settings, file, indent=4)
        return {'status': True, 'data': create_task_argument_data}
