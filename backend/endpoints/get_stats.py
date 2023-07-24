from datetime import datetime as dt
from datetime import timedelta as td

from flask import Flask

from database.interfaces import ChannelInterface
from database.interfaces import ProxyInterface
from database.interfaces import TaskInterface
from database.interfaces import TaskMakeInterface
from database.interfaces import TgClientInterface

from decorators.flask import is_logged_in_flask_decorator


def add_get_stats(app: Flask):
    @app.route("/get_stats", methods=['POST'])
    @is_logged_in_flask_decorator
    def get_stats():
        one_day = dt.utcnow() - td(days=1)
        one_week = dt.utcnow() - td(weeks=1)
        all_tasks = TaskInterface.get_all_by_()
        count_not_ready_tasks = 0
        for task in all_tasks:
            count_make = TaskMakeInterface.get_count_by_task_id_and_status(True, task.id)
            if count_make < task.required_count:
                count_not_ready_tasks += 1
        return {
            "status": True,
            "data": [
                TgClientInterface.get_count_by_(),
                TgClientInterface.get_count_by_is_banned(True),
                TgClientInterface.get_count_by_creation_time_less(one_week),
                ProxyInterface.get_count_by_(),
                ChannelInterface.get_count_by_(),
                TaskMakeInterface.get_count_by_time_less(one_day),
                TaskMakeInterface.get_count_by(),
                count_not_ready_tasks
            ]
        }
