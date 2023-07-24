import asyncio
import json
import os

import requests
from datetime import datetime as dt
from random import randint
from random import shuffle

import requests
from celery import Celery
from pathlib import Path

from database.interfaces import ChannelInterface
from database.interfaces import ProxyInterface
from database.interfaces import SubscriberInterface
from database.interfaces import TaskArgumentInterface
from database.interfaces import TaskInterface
from database.interfaces import AvatarInterface
from database.interfaces import TaskMakeInterface
from database.interfaces import TgClientInterface
from sms_activate import SmsActivateClient
from telegram_client import TelegramMyClient

import cyrtranslit
from pyrogram import Client
from time import sleep

from datetime import timedelta as td

from database.interfaces import TgAppInterface
from database.interfaces import DeviceInterface
from database.interfaces import UNameInterface

from random import choice
from random import choices
from string import ascii_letters
from vk_parser import get_all_group_followers
from vk_parser import get_all_user_followers
from threading import Thread
from database.interfaces import TaskForMakeInterface

celery_app = Celery(broker="redis://127.0.0.1:6379/8", backend="redis://127.0.0.1:6379/9")

clients_pool = {}



def get_client_by_phone_number(phone_number: int | str):
    while True:
        if not phone_number in clients_pool:
            clients_pool.update({
                phone_number: {
                    "client": TelegramMyClient(int(phone_number)),
                    "status": False
                }
            })
        if clients_pool[phone_number]['status']:
            print(clients_pool[phone_number])
            sleep(1)
            continue
        else:
            clients_pool[phone_number].update({
                "status": True
            })
            return clients_pool[phone_number]['client']


def stop_work_client(phone_number: int | str):
    sleep(1)
    clients_pool[phone_number].update({
        "status": False
    })


async def done_tasks():
    """Закрытие задач async loop"""
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(f'> {task.get_name()}')
        task.done()


def get_channel_model(channel_link_or_id: int | str):
    if type(channel_link_or_id) == str:
        channel_link_or_id = channel_link_or_id.replace("@", "https://t.me/")
        if channel_link_or_id.replace("-", "").isdigit():
            channel_model = ChannelInterface.get_first_by_channel_id(int(channel_link_or_id))
        else:
            channel_model = ChannelInterface.get_first_by_channel_invite_link(
                channel_link_or_id.replace("joinchat/", "+"))
    else:
        channel_model = ChannelInterface.get_first_by_channel_id(int(channel_link_or_id))
    return channel_model


@celery_app.task()
def check_proxy(proxy_id):
    """Проверка прокси на работоспособность"""

    def check_proxy(proxy_id):
        proxy_status = False
        proxy = ProxyInterface.get_first_by_id(proxy_id)
        try:
            proxy_string = f"{proxy.type}://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}" if proxy.username and proxy.password else f"{proxy.type}://{proxy.ip}:{proxy.port}"
            response = requests.get("https://t.me/", proxies={
                "http": proxy_string,
                "https": proxy_string
            }, timeout=5)
            if response.status_code == 200:
                proxy_status = True
        except:
            pass
        ProxyInterface.update_model_by_id(proxy.id, "last_use", dt.utcnow())
        if not proxy_status:
            ProxyInterface.update_model_by_id(proxy.id, "is_active", False)
            proxy_tg_clients = TgClientInterface.get_all_by_proxy_id(proxy.id)
            for proxy_tg_client in proxy_tg_clients:
                new_proxy = ProxyInterface.get_random_active_proxy()
                TgClientInterface.update_model_by_id(proxy_tg_client.id, "proxy_id", new_proxy.id)
        else:
            ProxyInterface.update_model_by_id(proxy.id, "is_active", True)

    Thread(target=check_proxy, args=(proxy_id,)).start()


@celery_app.task()
def check_account(phone_number, account_id):
    """Проверка аккаунта на работоспособность"""

    def check_account(phone_number, account_id):
        client = TelegramMyClient(phone_number)
        is_ban = client.check_account_is_banned()
        TgClientInterface.update_model_by_id(account_id, "is_ban", is_ban)

    Thread(target=check_account, args=(phone_number, account_id,)).start()


@celery_app.task()
def make_create_account_task(task_id: int, sms_activate_api_key: str, count_required: int):
    """Выполнение задачи по регистрации аккаунтов"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if count_required > 0:
        try:
            sms_activate_client = SmsActivateClient(sms_activate_api_key)
            if sms_activate_client.get_balance() >= sms_activate_client.get_countries_prices_array_telegram()[6]:
                activation_id, phone = sms_activate_client.get_telegram_number()
                tg_app = TgAppInterface.get_rand_()
                device = DeviceInterface.get_rand_()
                proxy_model = ProxyInterface.get_random_active_proxy()
                gender = choice(
                    [
                        "Male",
                        "Female"
                    ]
                )
                fname = UNameInterface.get_rand_by_type_and_gender('firstname', gender)
                lname = UNameInterface.get_rand_by_type_and_gender('lastname', gender)
                sname = UNameInterface.get_rand_by_type_and_gender('surname', gender)
                client = Client("client", api_id=tg_app.app_id,
                                api_hash=tg_app.app_hash,
                                app_version=tg_app.app_version,
                                device_model=device.device_model,
                                system_version=device.system_version,
                                proxy={
                                    "scheme": proxy_model.type,
                                    "hostname": proxy_model.ip,
                                    "port": proxy_model.port,
                                    "username": proxy_model.username if proxy_model.username else None,
                                    "password": proxy_model.password if proxy_model.password else None
                                }, in_memory=True)
                try:
                    client.connect()
                except Exception as ex:
                    print(ex)
                    if activation_id:
                        sms_activate_client.ban_number(activation_id)
                    make_create_account_task(task_id, sms_activate_api_key, count_required)
                    try:
                        loop.run_until_complete(done_tasks())
                    except Exception as ex:
                        print(f"Cannot stop loop: {ex}")
                    return
                try:
                    code_hash = client.send_code(phone)
                except Exception as ex:
                    print(ex)
                    if activation_id:
                        sms_activate_client.ban_number(activation_id)
                    make_create_account_task(task_id, sms_activate_api_key, count_required)
                    try:
                        loop.run_until_complete(done_tasks())
                    except Exception as ex:
                        print(f"Cannot stop loop: {ex}")
                    return
                print(code_hash)
                # if not "SMS" in str(code_hash.type):
                #     # if "APP" in str(code_hash.type):
                #     #     code_hash = client.resend_code(phone, code_hash.phone_code_hash)
                #     #     print(code_hash)
                #     if not "SMS" in str(code_hash.type):
                #         if activation_id:
                #             sms_activate_client.ban_number(activation_id)
                #         make_create_account_task(task_id, sms_activate_api_key, count_required)
                #         # try:
                #         #     loop.run_until_complete(done_tasks())
                #         # except Exception as ex:
                #         #     print(f"Cannot stop loop: {ex}")
                #         return

                start_time = dt.now()
                while True:
                    sleep(5)
                    now = dt.now()
                    code = sms_activate_client.get_number_status(activation_id)
                    print(code)
                    if not code:
                        if now - start_time > td(minutes=3):
                            if activation_id:
                                sms_activate_client.ban_number(activation_id)
                            make_create_account_task(task_id, sms_activate_api_key, count_required)
                            try:
                                loop.run_until_complete(done_tasks())
                            except Exception as ex:
                                print(f"Cannot stop loop: {ex}")
                            return
                    else:
                        try:
                            client.sign_in(phone_number=str(phone),
                                           phone_code_hash=code_hash.phone_code_hash,
                                           phone_code=code)
                            client.sign_up(phone_number=phone,
                                           phone_code_hash=code_hash.phone_code_hash,
                                           first_name=fname.value, last_name=lname.value)

                        except:
                            pass
                        session_string = client.export_session_string()
                        try:
                            client.disconnect()
                        except:
                            pass

                        response = requests.get(
                            f"https://www.namegeneratorfun.com/api/namegenerator?generatorType=list&minLength=7&maxLength=11&sexId=1&generatorId=161&userFirstName={cyrtranslit.to_latin(fname.value)}&userLastName={cyrtranslit.to_latin(lname.value)}").json()
                        username = choice(response['names']) + ''.join(choices(ascii_letters, k=3))
                        tg_client_id = TgClientInterface.create_model(
                            str(session_string),
                            phone,
                            tg_app.id,
                            device.id,
                            fname.id,
                            lname.id,
                            sname.id,
                            username,
                            False,
                            proxy_model.id
                        )
                        sms_activate_client.confirm_number(activation_id)
                        TaskMakeInterface.create_model(
                            task_id,
                            tg_client_id,
                            True
                        )
                        make_create_account_task(task_id, sms_activate_api_key, count_required - 1)
                        try:
                            loop.run_until_complete(done_tasks())
                        except Exception as ex:
                            print(f"Cannot stop loop: {ex}")
                        return True
            else:
                try:
                    loop.run_until_complete(done_tasks())
                except Exception as ex:
                    print(f"Cannot stop loop: {ex}")
                return False
        except Exception as ex:
            print(ex)
            try:
                loop.run_until_complete(done_tasks())
            except Exception as ex:
                print(f"Cannot stop loop: {ex}")
            make_create_account_task(task_id, sms_activate_api_key, count_required)


@celery_app.task()
def make_subscribe_task(task_id: int, client_phone_number: str | int, channel_link: str, is_active: bool,
                        read_last_posts: bool):
    """Выполнение задачи по подписке"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        print(f"SUBSCRIBE {client_phone_number} TO {channel_link}")
        client = TelegramMyClient(client_phone_number)
        task_make_status = client.join_channel(channel_link)
        client_model = TgClientInterface.get_first_by_phone_number(str(client_phone_number))
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        channel_model = get_channel_model(channel_link)
        with open("checker_subscribes.txt", 'r') as file:
            checker_subscribes = file.read().split("\n")
        if not str(channel_model.channel_id) in checker_subscribes:
            with open("subscribe_checker.txt", 'r') as file:
                session_string = file.read()
            checker_client = Client("checker", 8, "7245de8e747a0d6fbe11f7cc14fcc0bb", session_string=session_string,
                                    in_memory=True)
            try:
                checker_client.connect()
            except:
                pass
            channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
            try:
                chat_link = channel_link.replace("https://t.me/", "@") if not channel_link.count(
                    "joinchat/") else channel_link
                checker_client.join_chat(chat_link)
                with open("checker_subscribes.txt", 'a') as file:
                    file.write(str(channel_model.channel_id) + "\n")
            except Exception as ex:
                print("EXCEPT: " + str(ex))
            try:
                checker_client.disconnect()
            except:
                pass
        if read_last_posts:
            messages = client.get_last_messages(channel_model.channel_id, randint(5, 20))
            messages.reverse()
            idx = 0
            for message in messages:
                print(f"READ {channel_link}/{message.id} FROM {client.tg_client_settings.phone_number,}")
                TaskForMakeInterface.create_model("make_view_task", (
                    0,
                    client.tg_client_settings.phone_number,
                    channel_model.channel_id,
                    message.id,
                ), dt.utcnow() + td(seconds=idx * 60))
                idx += 1
        if not SubscriberInterface.check_user_is_subscriber(channel_model.id, client_model.id):
            SubscriberInterface.create_subscriber(
                channel_id=channel_model.id,
                tg_client_id=client_model.id,
                active_view=is_active
            )


@celery_app.task()
def make_unsubscribe_task(task_id: int, client_phone_number: str | int, channel_link: str):
    """Выполнение задачи по отписке"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        print(f"UNSUBSCRIBE {channel_link}")
        channel_model = get_channel_model(channel_link)
        client = TelegramMyClient(client_phone_number)
        task_make_status = client.leave_channel(channel_model.channel_id)
        client_model = TgClientInterface.get_first_by_phone_number(str(client_phone_number))
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        SubscriberInterface.delete_by_model_id(
            channel_model.id,
            client_model.id
        )


@celery_app.task()
def make_view_task(task_id: int, client_phone_number: str | int, channel_link: str, post_id: int):
    """Выполнение задачи на просмотры"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        print(f"VIEW POST {channel_link}/{post_id}")
        channel_model = get_channel_model(channel_link)

        client = TelegramMyClient(client_phone_number)
        task_make_status = client.send_view(channel_model.channel_id, post_id)
        client_model = TgClientInterface.get_first_by_phone_number(client_phone_number)
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        if not SubscriberInterface.check_user_is_subscriber(
                channel_model.id,
                client_model.id
        ):
            SubscriberInterface.create_subscriber(channel_model.id, client_model.id, False)


@celery_app.task()
def make_reaction_task(task_id: int, client_phone_number: str | int, channel_link: str, post_id: int, reaction: str):
    """Выполнение задачи на реакции"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        print(f"REACTION {reaction} TO {channel_link}/{post_id}")
        channel_model = get_channel_model(channel_link)
        client = TelegramMyClient(client_phone_number)
        task_make_status = client.send_reaction(channel_model.channel_id, post_id, reaction)
        client_model = TgClientInterface.get_first_by_phone_number(client_phone_number)
        if not SubscriberInterface.check_user_is_subscriber(
                channel_model.id,
                client_model.id
        ):
            SubscriberInterface.create_subscriber(channel_model.id, client_model.id, False)
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        


@celery_app.task()
def make_click_button_task(task_id: int, client_phone_number: str | int, channel_link: str, post_id: int,
                           button_id: int):
    """Выполнение задачи на нажатие кнопки в голосвании"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        client = TelegramMyClient(client_phone_number)
        channel_model = get_channel_model(channel_link)
        task_make_status = client.send_click(channel_model.channel_id, post_id, button_id)
        client_model = TgClientInterface.get_first_by_phone_number(client_phone_number)
        if not SubscriberInterface.check_user_is_subscriber(
                channel_model.id,
                client_model.id
        ):
            SubscriberInterface.create_subscriber(channel_model.id, client_model.id, False)
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        


@celery_app.task()
def make_comment_task(task_id: int, client_phone_number: str | int, channel_link: str, post_id: int, comment: str):
    """Выполнение задачи на комментарии"""
    if TaskInterface.get_first_by_id(task_id) or int(task_id) == 0:
        client = TelegramMyClient(client_phone_number)
        channel_model = get_channel_model(channel_link)
        task_make_status = client.send_comment(channel_model.channel_id, post_id, comment)
        client_model = TgClientInterface.get_first_by_phone_number(client_phone_number)
        if not SubscriberInterface.check_user_is_subscriber(
                channel_model.id,
                client_model.id
        ):
            SubscriberInterface.create_subscriber(channel_model.id, client_model.id, False)
        if task_make_status is None:
            task_make_status = False
        TaskMakeInterface.create_model(
            task_id,
            client_model.id,
            task_make_status
        )
        


@celery_app.task()
def save_photo(avatar_model):
    """Сохранение фотографии по ссылке"""
    avatar_name = ''.join(choices(ascii_letters, k=10)) + ".png"
    avatar_path = Path(Path.cwd(), "avatars", avatar_name)
    response = requests.get(avatar_model['download_href'], allow_redirects=True)
    with open(avatar_path, 'wb') as file:
        file.write(response.content)
    AvatarInterface.update_avatar_by_id(avatar_model['id'], "path_to_file", str(avatar_path))


@celery_app.task()
def parse_vk(link: str, profile_type: str):
    """Парсинг VK профилей и групп"""
    if profile_type == "user":
        get_all_user_followers(link[link.rfind("/") + 1:])
    else:
        get_all_group_followers(link[link.rfind("/") + 1:])