from flask import Flask
from flask import request

from database.interfaces import TaskInterface

from decorators.flask import is_logged_in_flask_decorator


def add_create(app: Flask):
    @app.route('/task/create', methods=['POST'])
    @is_logged_in_flask_decorator
    def task_create():
        form_data = request.form
        if not form_data.get('task_model_name') or not form_data.get('task_model_type') or not form_data.get(
                'task_model_required_count'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        task_model_name = form_data.get('task_model_name')
        task_model_type = form_data.get('task_model_type')
        task_model_required_count = form_data.get('task_model_required_count')
        create_task_data = TaskInterface.create_model(
            task_model_name=task_model_name, task_model_type=task_model_type,
            task_model_required_count=task_model_required_count, )
        return {'status': True, 'data': create_task_data}
