from celery_tasks import make_create_account_task
from celery_tasks import make_subscribe_task
from celery_tasks import make_unsubscribe_task
from celery_tasks import make_view_task
from celery_tasks import make_reaction_task
from celery_tasks import make_click_button_task
from celery_tasks import make_comment_task
from celery_tasks import save_photo
from celery_tasks import parse_vk
from database.interfaces import TaskForMakeInterface
from multiprocessing import Process
from app_init import get_settings
from time import sleep
from random import randint

from datetime import datetime as dt
from datetime import timedelta as td


def task_make():
    task_types = {
        "make_create_account_task": make_create_account_task,
        "make_subscribe_task": make_subscribe_task,
        "make_unsubscribe_task": make_unsubscribe_task,
        "make_view_task": make_view_task,
        "make_reaction_task": make_reaction_task,
        "make_click_button_task": make_click_button_task,
        "make_comment_task": make_comment_task,
        "save_photo": save_photo,
        "parse_vk": parse_vk
    }
    config = get_settings()
    active_processes = {}
    while True:
        tasks = TaskForMakeInterface.get_must_make_tasks()
        for task in tasks:
            while True:
                print(f"Count active processes: {len(active_processes)}")
                if len(active_processes) < config['max_count_processes']:
                    process = Process(target=task_types[task.task_type], args=task.task_arguments)
                    process.start()
                    process_id = randint(10 ** 6, 10 ** 7)
                    active_processes.update({
                        process_id: [process, dt.utcnow(), ]
                    })
                    Process(target=TaskForMakeInterface.delete_model_by_id, args=(task.id, )).start()
                    break
                removed_processes = []
                for key in active_processes:
                    if not active_processes[key][0].is_alive() or active_processes[key][1] + td(
                            minutes=5) < dt.utcnow():
                        removed_processes.append(key)
                        try:
                            active_processes[key][0].terminate()
                        except:
                            pass
                        try:
                            active_processes[key][0].join()
                        except:
                            pass
                for remove_process in removed_processes:
                    active_processes.pop(remove_process)
                sleep(1)
        sleep(1)


task_make()
