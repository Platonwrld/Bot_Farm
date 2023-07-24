from datetime import datetime as dt
from random import randint
from random import shuffle
from celery import Celery
from app_init import get_settings
from app_init import tg_bot

from database.interfaces import ChannelInterface
from database.interfaces import ProxyInterface
from database.interfaces import SubscriberInterface
from database.interfaces import TaskArgumentInterface
from database.interfaces import TaskInterface
from database.interfaces import AvatarInterface
from database.interfaces import TgClientInterface
from celery_tasks import check_proxy
from celery_tasks import check_account
from database.interfaces import TaskForMakeInterface
from _sheets import *
from datetime import timedelta as td

celery_app = Celery(broker="redis://127.0.0.1:6379/6", backend="redis://127.0.0.1:6379/7")


def parse_task_arguments(task_arguments: list):
    """Сбор всех аргументов задач в словарь"""
    parsed_task_arguments = {}
    for task_argument in task_arguments:
        parsed_task_arguments.update({
            task_argument.name: task_argument.value
        })
    return parsed_task_arguments


def check_task_date(task_arguments: dict):
    """Проверка возможности старта задачи по времени"""
    start_time = task_arguments.get("start_time")
    if not start_time:
        return False
    try:
        start_time = dt.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            start_time = dt.strptime(start_time, "%Y-%m-%d %H:%M")
        except:
            return False
    print(dt.utcnow())
    print(dt.utcnow() < start_time)
    if dt.now() < start_time:
        return False
    end_time = task_arguments.get("end_time")
    if not end_time:
        return False
    return True


def get_accounts_for_make(only_subscribers: bool | None, channel_link: str):
    """Получение аккаунтов для выполнения задачи"""
    accounts = TgClientInterface.get_all_not_banned()
    result_accounts = []
    channel = ChannelInterface.get_first_by_channel_invite_link(channel_link)
    for account in accounts:
        check_is_subscribe = True
        if only_subscribers is not None:
            if only_subscribers:
                check_is_subscribe = SubscriberInterface.check_user_is_subscriber(channel.id, account.id)
            else:
                check_is_subscribe = not SubscriberInterface.check_user_is_subscriber(channel.id, account.id)
        if check_is_subscribe:
            result_accounts.append({
                "phone_number": account.phone_number
            })
    return result_accounts


def update_accounts_data(req_keys_with_values: dict, accounts: list) -> list:
    """Обновление аккаунтов для выполнения определенных целей например отписки через время"""
    updated_keys = []
    for req_key in req_keys_with_values:
        count_added = 0
        for i in range(len(accounts)):
            account = accounts[i]
            if count_added < req_keys_with_values[req_key]:
                can_update_account = True
                for update_key in updated_keys:
                    if account.get(update_key):
                        accounts[i].update({req_key: False})
                        can_update_account = False
                        break
                if can_update_account:
                    accounts[i].update({req_key: True})
                    count_added += 1
            else:
                accounts[i].update({req_key: False})
        updated_keys.append(req_key)
    return accounts


def get_time_for_execute(execute_seconds, req_count, floating_speed):
    """Получение времени отведенного на одно выполнение задачи"""
    time_for_one_execute = int(execute_seconds / req_count)
    if floating_speed:
        time_for_one_execute += randint(0, 120)
    return time_for_one_execute


def parse_post_ids(post_ids_and_links: list[str]):
    """Сбор ID постов по ссылкам"""
    result_post_ids = []
    for post_id_and_link in post_ids_and_links:
        if str(post_id_and_link).isdigit():
            result_post_ids.append(int(post_id_and_link))
        else:
            post_id = post_id_and_link[post_id_and_link.rfind("/") + 1:]
            if post_id.isdigit():
                result_post_ids.append(int(post_id))
    return result_post_ids


@celery_app.task()
def check_accounts():
    """Проверка аккаунтов на блокировку"""
    print("Check accounts")
    config = get_settings()
    for admin_id in config['tg_bot_admins_ids']:
        try:
            tg_bot.send_message(admin_id, "🤖 Выполняю проверку аккаунтов на работоспособность")
        except Exception as ex:
            pass
    accounts = TgClientInterface.get_all_by_()
    for account in accounts:
        check_account(account.phone_number, account.id)


@celery_app.task()
def check_proxies():
    """Проверка прокси на работоспособность"""
    print("Check proxies")
    config = get_settings()
    for admin_id in config['tg_bot_admins_ids']:
        try:
            tg_bot.send_message(admin_id, "🌐 Выполняю проверку прокси на работоспособность")
        except Exception as ex:
            pass
    proxies = ProxyInterface.get_all_by()
    for proxy in proxies:
        check_proxy(proxy.id)


@celery_app.task()
def create_tasks_accounts_create():
    """Создание задач на регистрацию аккаунтов"""
    print("Create accounts")
    count_started = 0
    tasks = TaskInterface.get_all_by_task_type("accounts_create")
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            sms_activate_api_key = task_arguments.get("sms_activate_api_key")
            if sms_activate_api_key:
                TaskForMakeInterface.create_model("make_create_account_task",
                                                  (task.id, sms_activate_api_key, task.required_count, ), dt.utcnow())
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"🔑 Запущено {count_started} по регистрации аккаунтов")
            except Exception as ex:
                pass

@celery_app.task()
def create_tasks_subscribers():
    """Создание задач на подписку"""
    print("Subscribers")
    tasks = TaskInterface.get_all_by_task_type("subscribers")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue
            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds
            floating_speed = task_arguments.get("floating_speed") != "false"
            percent_active_subscribers = 0
            percent_moment_unsubscribes = int(task_arguments.get("percent_moment_unsubscribes"))
            percent_timer_unsubscribes = int(task_arguments.get("percent_t_unsubscribes"))
            read_last_posts = task_arguments.get("read_last_posts") != "false"
            channel_link = task_arguments.get("channel_link")

            accounts_for_make = get_accounts_for_make(False, channel_link)
            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            active_subscribers_count = int(req_count / 100 * percent_active_subscribers)
            moment_unsubscribes_count = int(
                (req_count - active_subscribers_count) / 100 * percent_moment_unsubscribes)
            timer_unsubscribes_count = int((
                                                   req_count - active_subscribers_count - moment_unsubscribes_count) / 100 * percent_timer_unsubscribes)
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]
            accounts_for_make = update_accounts_data({
                "is_active": active_subscribers_count,
                "is_moment_unsub": moment_unsubscribes_count,
                "is_timer_unsub": timer_unsubscribes_count
            }, accounts_for_make)
            TaskInterface.update_model_by_id(task.id, "required_count", req_count)
            shuffle(accounts_for_make)
            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                print(f"Subscribe {channel_link} at {dt.now() + td(seconds=time_for_one_execute * i)}")
                TaskForMakeInterface.create_model("make_subscribe_task", (task.id, account['phone_number'], channel_link, account['is_active'],
                          read_last_posts,), dt.utcnow() + td(seconds=time_for_one_execute * i))
                if account['is_moment_unsub']:
                    print(f"UNSUBSCRIBE {channel_link}/ at {dt.now() + td(seconds=time_for_one_execute * i + 30)}")
                    TaskForMakeInterface.create_model("make_unsubscribe_task",
                                                      (0, account['phone_number'], channel_link,),
                                                      dt.utcnow() + td(seconds=time_for_one_execute * i + 30))
                elif account['is_timer_unsub']:
                    timer = randint(60 * 60, 60 * 60 * 12)
                    print(f"UNSUBSCRIBE {channel_link}/ at {dt.now() + td(seconds=time_for_one_execute * i + timer)}")
                    TaskForMakeInterface.create_model("make_unsubscribe_task",
                                                      (0, account['phone_number'], channel_link,),
                                                      dt.utcnow() + td(seconds=time_for_one_execute * i + timer))
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"👥 Запущено {count_started} по подписке на группы")
            except Exception as ex:
                pass


@celery_app.task()
def create_tasks_remove_subscribers():
    """Создание задач на отписку"""
    print("Remove subscribers")
    tasks = TaskInterface.get_all_by_task_type("remove_subscribers")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue

            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds

            floating_speed = task_arguments.get("floating_speed") != "false"
            percent_returned = int(task_arguments.get("percent_returned"))
            channel_link = task_arguments.get("channel_link")

            accounts_for_make = get_accounts_for_make(True, channel_link)

            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]
            returned_subscribers_count = int(req_count / 100 * percent_returned)

            accounts_for_make = update_accounts_data({
                "is_return": returned_subscribers_count
            }, accounts_for_make)

            TaskInterface.update_model_by_id(task.id, "required_count", req_count)
            shuffle(accounts_for_make)
            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                print(f"UNSUBSCRIBE {channel_link}/ at {dt.now() + td(seconds=time_for_one_execute * i)}")
                TaskForMakeInterface.create_model("make_unsubscribe_task", (task.id, account['phone_number'], channel_link,), dt.utcnow() + td(seconds=time_for_one_execute * i))
                if account['is_return']:
                    timer = randint(60 * 60, 60 * 60 * 12)
                    print(f"Subscribe {channel_link}/ at {dt.now() + td(seconds=time_for_one_execute * i + timer)}")
                    TaskForMakeInterface.create_model("make_subscribe_task", (0, account['phone_number'], channel_link, False,
                              True,), dt.utcnow() + td(seconds=time_for_one_execute * i + timer))
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"🔙 Запущено {count_started} по отписке с групп")
            except Exception as ex:
                pass


@celery_app.task()
def create_tasks_views():
    """Создание задач на просмотры"""
    print("Views")
    tasks = TaskInterface.get_all_by_task_type("views")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue

            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds

            floating_speed = task_arguments.get("floating_speed") != "false"
            posts_ids = parse_post_ids(task_arguments.get("posts_ids").split("\n"))

            only_subscribers = task_arguments.get("only_subscribers") != "false"
            channel_link = task_arguments.get("channel_link")

            accounts_for_make = get_accounts_for_make(True if only_subscribers else None, channel_link)

            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]

            TaskInterface.update_model_by_id(task.id, "required_count", req_count)
            shuffle(accounts_for_make)
            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                for post_id in posts_ids:
                    print(f"View {channel_link}/ at {dt.now() + td(seconds=time_for_one_execute * i)}")
                    TaskForMakeInterface.create_model("make_view_task",
                                                      (task.id, account['phone_number'], channel_link, post_id,),
                                                      dt.utcnow() + td(time_for_one_execute * i))
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"👁 Запущено {count_started} по просмотру постов в группах")
            except Exception as ex:
                pass


@celery_app.task()
def create_tasks_reactions():
    """Создание задач на реакции"""
    print("Reactions")
    tasks = TaskInterface.get_all_by_task_type("reactions")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue

            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds

            floating_speed = task_arguments.get("floating_speed") != "false"
            posts_ids = parse_post_ids(task_arguments.get("posts_ids").split("\n"))
            emoji_now = task_arguments.get("emoji_now")
            only_subscribers = task_arguments.get("only_subscribers") != "false"
            channel_link = task_arguments.get("channel_link")

            accounts_for_make = get_accounts_for_make(True if only_subscribers else None, channel_link)

            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]

            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                for post_id in posts_ids:
                    print(f"Reaction {channel_link}/{post_id} at {dt.now() + td(seconds=time_for_one_execute * i)}")
                    TaskForMakeInterface.create_model("make_reaction_task", (task.id, account['phone_number'],
                                                                             channel_link, post_id, emoji_now,),
                                                      dt.utcnow() + td(seconds=time_for_one_execute * i))
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"👍 Запущено {count_started} по реакциям на посты в группах")
            except Exception as ex:
                pass


@celery_app.task()
def create_tasks_votes():
    """Создание задач на голосования"""
    print("Votes")
    tasks = TaskInterface.get_all_by_task_type("votes")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue

            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds

            floating_speed = task_arguments.get("floating_speed") != "false"
            posts_ids = parse_post_ids(task_arguments.get("posts_ids").split("\n"))
            vote_number = int(task_arguments.get("vote_number"))
            channel_link = task_arguments.get("channel_link")
            only_subscribers = task_arguments.get("only_subscribers") != "false"

            accounts_for_make = get_accounts_for_make(True if only_subscribers else None, channel_link)

            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]

            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                for post_id in posts_ids:
                    print(f"Click button {channel_link}/{post_id} at {dt.now() + td(seconds=time_for_one_execute * i)}")
                    TaskForMakeInterface.create_model("make_click_button_task",
                                                      (task.id, account['phone_number'], channel_link, post_id,
                                                       vote_number,), dt.utcnow() + td(seconds=time_for_one_execute *
                                                                                               i))
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"🗣 Запущено {count_started} по голосованию постов в группах")
            except Exception as ex:
                pass


@celery_app.task()
def create_tasks_comments():
    """Создание задач на комментарии"""
    print("Comments")
    tasks = TaskInterface.get_all_by_task_type("comments")
    count_started = 0
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            if not check_task_date(task_arguments):
                TaskInterface.update_model_by_id(task.id, "is_activate", False)
                continue

            try:
                start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    start_time = dt.strptime(task_arguments.get("start_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            try:
                end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    end_time = dt.strptime(task_arguments.get("end_time"), "%Y-%m-%d %H:%M")
                except:
                    TaskInterface.update_model_by_id(task.id, "is_activate", False)
                    continue
            execute_seconds = (end_time - start_time).seconds

            floating_speed = task_arguments.get("floating_speed") != "false"
            posts_ids = parse_post_ids(task_arguments.get("posts_ids").split("\n"))
            comment_texts = task_arguments.get("comment_text").split("|")
            only_subscribers = task_arguments.get("only_subscribers") != "false"
            repeat_comments = task_arguments.get("read_last_posts") != "false"
            channel_link = task_arguments.get("channel_link")

            accounts_for_make = get_accounts_for_make(True if only_subscribers else None, channel_link)

            req_count = len(accounts_for_make) if len(
                accounts_for_make) < task.required_count else task.required_count
            if not repeat_comments:
                req_count = req_count if req_count < len(comment_texts) else len(comment_texts)
            if len(accounts_for_make) > req_count:
                accounts_for_make = accounts_for_make[:req_count]
            idx = 0
            for i in range(len(accounts_for_make)):
                time_for_one_execute = get_time_for_execute(execute_seconds, req_count, floating_speed)
                account = accounts_for_make[i]
                for post_id in posts_ids:

                    if repeat_comments:
                        shuffle(comment_texts)
                        comment_text = comment_texts[0]
                    else:
                        comment_text = comment_texts.pop(0)
                    print(f"COMMENT {channel_link}/{post_id} at {dt.now() + td(seconds=time_for_one_execute * idx)}")
                    TaskForMakeInterface.create_model("make_comment_task", (task.id, account['phone_number'],
                                                                            channel_link, post_id, comment_text,),
                                                      dt.utcnow() + td(seconds=time_for_one_execute * idx))
                    idx += 1
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"✉️ Запущено {count_started} по написанию комментов в группах")
            except Exception as ex:
                pass


def synchronization_google_sheets_one(table, model):
    """Синхронизация одной таблицы Google Sheets"""
    try:
        delete_from_table(table, model.__tablename__)
    except Exception as ex:
        print(f"ERROR DELETE {ex}")
        print(model.__tablename__)
    try:
        add_to_table(table, model.__tablename__)
    except Exception as ex:
        print(f"ERROR ADD {ex}")
        print(model.__tablename__)
    try:
        update_from_table(table, model.__tablename__)
    except Exception as ex:
        print(f"ERROR UPDATE {ex}")
        print(model.__tablename__)
    try:
        synchronize_table(table, model.__tablename__)
    except Exception as ex:
        print(f"ERROR SYNCHRONIZE {ex}")
        print(model.__tablename__)


@celery_app.task()
def synchronization_google_sheets():
    """Синхронизация всех таблиц Google Sheets"""
    print("Google Sheets synchrone")
    config = get_settings()
    for admin_id in config['tg_bot_admins_ids']:
        try:
            tg_bot.send_message(admin_id, f"🗂 Запущена синхронизация с Google Таблицей")
        except Exception as ex:
            pass
    create_not_exists_sheets(table)
    for model in models:
        if not model.__tablename__ in ignore_tablenames:
            try:
                synchronization_google_sheets_one(table, model, )
            except Exception as ex:
                print(ex)
                print(model.__tablename__)
            print(f"GOOGLE SHEETS END SYNCHRONE {model.__tablename__}")
    print("END GOOGLE SHEETS SYNCHRONE")


@celery_app.task()
def download_avatars():
    """Скачивание аватаров"""
    print("Download avatars")
    avatars = AvatarInterface.get_all_by_has_not_path()
    for avatar in avatars:
        TaskForMakeInterface.create_model("save_photo", (avatar.to_dict(), ), dt.utcnow())


@celery_app.task()
def create_tasks_parse_vk():
    """Создание задач на парсинг ВК"""
    print("Parse VK")
    count_started = 0
    tasks = TaskInterface.get_all_by_task_type("parse_vk")
    for task in tasks:
        if not task.is_activate:
            TaskInterface.update_model_by_id(task.id, "is_activate", True)
            list_task_arguments = TaskArgumentInterface.get_all_by_task_id(
                task.id
            )
            task_arguments = parse_task_arguments(list_task_arguments)
            link = task_arguments.get("profile_link")
            profile_type = task_arguments.get("profile_type")
            if link and profile_type:
                TaskForMakeInterface.create_model("parse_vk", (link, profile_type), dt.utcnow())
            count_started += 1
    config = get_settings()
    if config['is_null_notificated'] or count_started > 0:
        for admin_id in config['tg_bot_admins_ids']:
            try:
                tg_bot.send_message(admin_id, f"✏️ Запущено {count_started} заданий по парсингу VK")
            except Exception as ex:
                pass


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Создание переодических задач в Celery"""
    celery_app.add_periodic_task(60.0 * 60 * 24, check_accounts.s())
    celery_app.add_periodic_task(60.0 * 60 * 24, check_proxies.s())
    celery_app.add_periodic_task(60.0, create_tasks_accounts_create.s())
    celery_app.add_periodic_task(60.0, create_tasks_subscribers.s())
    celery_app.add_periodic_task(60.0, create_tasks_remove_subscribers.s())
    celery_app.add_periodic_task(60.0, create_tasks_views.s())
    celery_app.add_periodic_task(60.0, create_tasks_reactions.s())
    celery_app.add_periodic_task(60.0, create_tasks_votes.s())
    celery_app.add_periodic_task(60.0, create_tasks_comments.s())
    celery_app.add_periodic_task(60.0 * 10, synchronization_google_sheets.s())
    celery_app.add_periodic_task(60.0, create_tasks_parse_vk.s())

create_tasks_subscribers.delay()
create_tasks_accounts_create.delay()
create_tasks_subscribers.delay()
create_tasks_remove_subscribers.delay()
create_tasks_views.delay()
create_tasks_reactions.delay()
create_tasks_votes.delay()
create_tasks_comments.delay()
create_tasks_parse_vk.delay()
synchronization_google_sheets.delay()
