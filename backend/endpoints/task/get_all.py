from math import ceil

from flask import Flask
from flask import request

from database.interfaces import TaskArgumentInterface
from database.interfaces import TaskInterface
from database.interfaces import TaskMakeInterface

from decorators.flask import is_logged_in_flask_decorator


def add_get_all(app: Flask):
    @app.route('/task/get_pagination', methods=['POST'])
    @is_logged_in_flask_decorator
    def task_get_all():
        form_data = request.form
        if not form_data.get('page'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        page = form_data.get('page')
        tmp_tasks = TaskInterface.get_pagination_by_(10, int(page))
        count_tasks = TaskInterface.get_count_by_()
        tasks = []
        for tmp_task in tmp_tasks:
            task = tmp_task.to_dict()
            count_makes = TaskMakeInterface.get_count_by_task_id_and_status(True, tmp_task.id)
            tmp_task_args = TaskArgumentInterface.get_all_by_task_id(tmp_task.id)
            for tmp_task_arg in tmp_task_args:
                task.update({
                    tmp_task_arg.name: tmp_task_arg.value
                })
            task.update({
                "count_makes": count_makes
            })
            tasks.append(task)
        return {
            "status": True,
            "data": {
                "tasks": tasks,
                "count_pages": ceil(count_tasks / 10)
            }
        }
