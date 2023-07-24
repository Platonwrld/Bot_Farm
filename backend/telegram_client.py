import asyncio
import os

import requests
from pyrogram import Client as TelegramClient
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram.raw.functions.account import UpdateStatus

from database.interfaces import DeviceInterface
from database.interfaces import ProxyInterface
from database.interfaces import TgAppInterface
from database.interfaces import TgClientInterface
from database.interfaces import UNameInterface
from database.interfaces import BioInterface
from database.interfaces import NicknameInterface
from database.interfaces import AvatarInterface
from random import randint
from datetime import datetime as dt
from datetime import timedelta as td
from pathlib import Path
from random import choices
from string import ascii_letters


async def done_tasks():
    """Закрытие задач async loop"""
    tasks = asyncio.all_tasks()
    for task in tasks:
        task.get_name()
        task.done()


def check_proxy(tg_client_id, proxy_model, is_change=False):
    try:
        response = requests.get("https://t.me/", proxies={
            "http": f"{proxy_model.type}://{f'{proxy_model.username}:{proxy_model.password}@' if proxy_model.username and proxy_model.password else ''}{proxy_model.ip}:{proxy_model.port}",
            "https": f"{proxy_model.type}://{f'{proxy_model.username}:{proxy_model.password}@' if proxy_model.username and proxy_model.password else ''}{proxy_model.ip}:{proxy_model.port}",
        }, timeout=5)
        if response.status_code != 200:
            return change_and_check_proxy(tg_client_id, proxy_model)
        print(f"GOOD {proxy_model.ip}:{proxy_model.port}")
        return not is_change
    except:
        print(f"BAD {proxy_model.ip}:{proxy_model.port}")
        return change_and_check_proxy(tg_client_id, proxy_model)


def change_and_check_proxy(tg_client_id: int, proxy_model):
    ProxyInterface.update_model_by_id(proxy_model.id, "last_use", dt.utcnow())
    new_proxy = ProxyInterface.get_random_active_proxy()
    TgClientInterface.update_model_by_id(tg_client_id, "proxy_id", new_proxy.id)
    return check_proxy(tg_client_id, new_proxy, is_change=True)


class TelegramMyClient:
    def __init__(self, phone_number: int):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.phone_number = phone_number
        self.tg_client_settings = TgClientInterface.get_first_by_phone_number(str(phone_number))
        tg_app_model = TgAppInterface.get_first_by_id(self.tg_client_settings.tg_app_id)
        device_model = DeviceInterface.get_first_by_id(self.tg_client_settings.device_id)
        proxy_model = ProxyInterface.get_first_by_id(self.tg_client_settings.proxy_id)
        self.u_fname_model = UNameInterface.get_first_by_id(self.tg_client_settings.u_fname_id)
        check_proxy(self.tg_client_settings.id, proxy_model)
        self.client = TelegramClient("client",
                                     session_string=self.tg_client_settings.client_hash,
                                     api_id=tg_app_model.app_id,
                                     api_hash=tg_app_model.app_hash,
                                     app_version=tg_app_model.app_version,
                                     device_model=device_model.device_model,
                                     system_version=device_model.system_version,
                                     proxy={
                                         "scheme": proxy_model.type,
                                         "hostname": proxy_model.ip,
                                         "port": int(proxy_model.port),
                                         "username": proxy_model.username if proxy_model.username else None,
                                         "password": proxy_model.password if proxy_model.password else None
                                     },
                                     lang_code="ru",
                                     in_memory=True)
        if self.tg_client_settings.creation_time < dt.utcnow() - td(days=7):
            if not self.check_account_is_banned():
                if not self.tg_client_settings.is_nickname_and_bio_updated:
                    self.update_nickname_and_bio()
                if not self.tg_client_settings.is_avatar_updated:
                    self.update_avatar()

    def check_connection(self):
        """Проверка на подключение Telegram клиента"""
        try:
            proxy_model = ProxyInterface.get_first_by_id(self.tg_client_settings.proxy_id)
            if check_proxy(self.tg_client_settings.id, proxy_model):
                return self.client.is_connected
            else:
                self.__disconnect()
                self.tg_client_settings = TgClientInterface.get_first_by_phone_number(str(self.phone_number))
                tg_app_model = TgAppInterface.get_first_by_id(self.tg_client_settings.tg_app_id)
                device_model = DeviceInterface.get_first_by_id(self.tg_client_settings.device_id)
                proxy_model = ProxyInterface.get_first_by_id(self.tg_client_settings.proxy_id)
                self.u_fname_model = UNameInterface.get_first_by_id(self.tg_client_settings.u_fname_id)
                check_proxy(self.tg_client_settings.id, proxy_model)
                self.client = TelegramClient("client",
                                             session_string=self.tg_client_settings.client_hash,
                                             api_id=tg_app_model.app_id,
                                             api_hash=tg_app_model.app_hash,
                                             app_version=tg_app_model.app_version,
                                             device_model=device_model.device_model,
                                             system_version=device_model.system_version,
                                             proxy={
                                                 "scheme": proxy_model.type,
                                                 "hostname": proxy_model.ip,
                                                 "port": int(proxy_model.port),
                                                 "username": proxy_model.username if proxy_model.username else None,
                                                 "password": proxy_model.password if proxy_model.password else None
                                             },
                                             lang_code="ru",
                                             in_memory=True)
        except:
            pass

    def __connect(self):
        """Соединение с клиентом"""
        if not self.check_connection():
            try:
                self.client.connect()
                self.client.invoke(UpdateStatus(offline=False))
                return True
            except Exception as ex:
                print(f"Connection exception: {ex}")
                return False
        return False

    def __disconnect(self):
        """Разсоединение с клиентом"""
        try:
            self.client.disconnect()
        except:
            return

    def __del__(self):
        print("DELETE")
        self.__disconnect()
        self.loop.run_until_complete(done_tasks())


    def check_account_is_banned(self):
        """Проверка на то, аккаунт заблокирован в Tg или нет"""
        self.__connect()
        try:
            self.client.get_me()
            return False
        except:
            return True

    def update_avatar(self):
        """Обновление аватара клиента"""
        self.__connect()
        try:
            avatar_model = AvatarInterface.get_random_avatar(self.u_fname_model.gender.lower() == "male")
            avatar_name = ''.join(choices(ascii_letters, k=10)) + ".png"
            avatar_path = Path(Path.cwd(), "avatars", avatar_name)
            response = requests.get(avatar_model.download_href, allow_redirects=True, timeout=5)
            with open(avatar_path, 'wb') as file:
                file.write(response.content)
            if avatar_model:
                try:
                    self.client.set_profile_photo(photo=str(avatar_path))
                except:
                    pass
            os.remove(avatar_path)
        except Exception as ex:
            print(f"Cannot update avatar: {ex}")
        TgClientInterface.update_model_by_id(self.tg_client_settings.id, "is_avatar_updated", True)
        self.__disconnect()

    def update_nickname_and_bio(self):
        """Обновление имени / фамилии и биографии клиента"""
        self.__connect()
        nickname = NicknameInterface.get_random_nickname(self.u_fname_model.gender.lower() == "male")
        if nickname:
            bio = BioInterface.get_random_bio(self.u_fname_model.gender.lower() == "male")
            bio_text = None
            if bio:
                if randint(0, 1):
                    bio_text = bio.bio_text
            try:
                self.client.update_profile(nickname.first_name, nickname.last_name, bio_text)
            except Exception as ex:
                pass
            try:
                self.client.set_username(nickname.username)
                TgClientInterface.update_model_by_id(self.tg_client_settings.id, "username", nickname.username)
            except Exception as ex:
                if not "deleted" in str(ex).lower():
                    return self.update_nickname_and_bio()
                else:
                    TgClientInterface.delete_model_by_id(self.tg_client_settings.id)
            NicknameInterface.update_nickname_by_id(nickname.id, "is_used", True)
            TgClientInterface.update_model_by_id(self.tg_client_settings.id, "is_nickname_and_bio_updated", True)
        self.__disconnect()

    def get_chat_id(self, channel_link_or_id: int | str):
        """Получение ID чата Telegram"""
        self.__connect()
        if type(channel_link_or_id) == str:
            if not channel_link_or_id.replace("-", "").isdigit():
                channel_link_or_id = channel_link_or_id.replace("https", "http").replace("http", "https").replace("+",
                                                                                                                  "joinchat/")
                if not "joinchat/" in channel_link_or_id:
                    channel_link_or_id = channel_link_or_id.replace("https://t.me/", "@")
                try:
                    channel_link_or_id = self.client.get_chat(channel_link_or_id).id
                except:
                    pass
                try:
                    self.client.get_chat_member(channel_link_or_id, self.client.get_me().id)
                except:
                    try:
                        self.client.join_chat(channel_link_or_id)
                    except:
                        return False
                try:
                    channel_link_or_id = self.client.get_chat(channel_link_or_id).id
                    return channel_link_or_id
                except:
                    return False
        self.__disconnect()
        return int(channel_link_or_id)

    def join_channel(self, channel_link_or_id: int | str):
        return self.get_chat_id(channel_link_or_id) != False

    def leave_channel(self, channel_link_or_id: int | str):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            self.client.leave_chat(chat_id)
            self.__disconnect()
            return True
        except:
            self.__disconnect()
            return False

    def send_view(self, channel_link_or_id: int | str, post_id: int):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            self.client.invoke(
                GetMessagesViews(peer=self.client.resolve_peer(chat_id), id=[int(post_id), ], increment=True))
            self.__disconnect()
            return True
        except:
            self.__disconnect()
            return False

    def send_reaction(self, channel_link_or_id: int | str, post_id: int, reaction_type: str):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            self.client.send_reaction(chat_id, int(post_id), reaction_type)
            self.__disconnect()
            return True
        except:
            self.__disconnect()
            return False

    def send_comment(self, channel_link_or_id: int | str, post_id: int, comment_text: str):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            discussion_message = self.client.get_discussion_message(int(chat_id), int(post_id))
            discussion_message.reply(comment_text)
            self.__disconnect()
            return True
        except:
            self.__disconnect()
            return False

    def send_click(self, channel_link_or_id: int | str, post_id: int, button_id: int):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            message = self.client.get_messages(chat_id, [int(post_id), ])[0]
            idx = 1
            for i in range(len(message.reply_markup)):
                for j in range(len(message.reply_markup[i])):
                    if idx == button_id:
                        self.client.request_callback_answer(
                            chat_id=message.chat.id,
                            message_id=message.id,
                            callback_data=message.reply_markup[i][j].callback_data
                        )
                        self.__disconnect()
                        return True
                    idx += 1
            self.__disconnect()
            return False
        except:
            self.__disconnect()
            return False

    def get_last_messages(self, channel_link_or_id: int | str, count_messages: int):
        chat_id = self.get_chat_id(channel_link_or_id)
        self.__connect()
        try:
            messages_result = []
            for message in self.client.get_chat_history(chat_id, limit=count_messages):
                messages_result.append(message)
            self.__disconnect()
            return messages_result
        except:
            return []
