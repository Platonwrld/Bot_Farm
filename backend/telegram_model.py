import asyncio
import os

import requests
from pyrogram import Client as TelegramClient
from pyrogram.raw.functions.messages import GetMessagesViews

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

class TelegramMyClient:
    def __init__(self, telegram_number):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        telegram_number = str(telegram_number).replace(".session", "").replace(".json", "").replace("-journal", "")
        self.telegram_number = telegram_number
        self.tg_client_settings = TgClientInterface.get_first_by_phone_number(telegram_number)
        tg_app_model = TgAppInterface.get_first_by_id(self.tg_client_settings.tg_app_id)
        device_model = DeviceInterface.get_first_by_id(self.tg_client_settings.device_id)
        proxy_model = ProxyInterface.get_first_by_id(self.tg_client_settings.proxy_id)
        self.u_fname_model = UNameInterface.get_first_by_id(self.tg_client_settings.u_fname_id)
        u_lname_model = UNameInterface.get_first_by_id(self.tg_client_settings.u_lname_id)
        u_sname_model = UNameInterface.get_first_by_id(self.tg_client_settings.u_sname_id)
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
            if not self.tg_client_settings.is_nickname_and_bio_updated:
                self.update_nickname_and_bio()
            if not self.tg_client_settings.is_avatar_updated:
                self.update_avatar()

    def __check_connection(self):
        """Проверка на подключение Telegram клиента"""
        try:
            return self.client.is_connected
        except:
            pass

    def update_nickname_and_bio(self):
        """Обновление имени / фамилии и биографии клиента"""
        print(f"SET NICKNAME {self.tg_client_settings.phone_number}")
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

    def update_avatar(self):
        """Обновление аватара клиента"""
        print(f"SET AVATAR {self.tg_client_settings.phone_number}")
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

    def __connect(self):
        """Соединение с клиентом"""
        if not self.__check_connection():
            try:
                self.client.connect()
                return True
            except Exception as ex:
                return False
        return False

    def __disconnect(self):
        """Разсоединение с клиентом"""
        if self.telegram_number:
            try:
                self.client.disconnect()
            except Exception as ex:
                return

    def __del__(self):
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

    def check_user_is_subscriber(self, channel_link: str):
        """Проверка на то подписан ли клиент на группу или нет"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        self.__connect()
        try:
            self.client.get_chat_member(self.client.get_chat(channel_link).id, self.client.get_me().id)
            return True
        except Exception as ex:
            return False

    def join_channel(self, channel_link: str):
        """Вступление клиента в канал"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        if not self.check_user_is_subscriber(channel_link):
            try:
                self.__connect()
                self.client.join_chat(channel_link)
                self.__disconnect()
                return True
            except Exception as ex:
                print(ex)
                return False

    def get_channel_data(self, channel_link: str):
        """Получение данных о канали по ссылке"""
        try:
            self.join_channel(channel_link)
            self.__connect()
            channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
            if not "joinchat/" in channel_link:
                channel_link = channel_link.replace("https://t.me/", "@")
            chat_data = self.client.get_chat(channel_link)
            self.__disconnect()
            return chat_data
        except:
            return False

    def send_message(self, chat: str, text: str):
        """Отправка сообщения клиентом"""
        try:
            self.__connect()
            self.client.send_message(chat, text)
            self.__disconnect()
        except:
            pass

    def unsubscribe(self, channel_link: str):
        """Отписка от канала клиентом"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        try:
            self.join_channel(channel_link)
            self.__connect()
            if not channel_link.replace("-", "").isdigit():
                chat = self.client.get_chat(channel_link)
            self.client.leave_chat(chat.id)
            self.__disconnect()
            return True
        except:
            return False

    def send_reaction(self, channel_link: str, post_id: int, reaction_type):
        """Отправка реакции клиентом"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        try:
            self.join_channel(channel_link)
            self.__connect()
            if not channel_link.replace("-", "").isdigit():
                chat = self.client.get_chat(channel_link)
            self.client.send_reaction(chat.id, int(post_id), reaction_type)
            self.__disconnect()
            return True
        except Exception as ex:
            print(ex)
            return False

    def send_view(self, channel_link: str, post_id: int):
        """Отправка просмотра клиентом"""
        if type(channel_link) == str:
            channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
            if not "joinchat/" in channel_link:
                channel_link = channel_link.replace("https://t.me/", "@")
        try:
            if type(channel_link) == str:
                self.join_channel(channel_link)
            self.__connect()
            if type(channel_link) == str:
                if not channel_link.replace("-", "").isdigit():
                    chat = self.client.get_chat(channel_link)
                    self.client.invoke(
                        GetMessagesViews(peer=self.client.resolve_peer(int(chat.id)), id=[int(post_id), ], increment=True))
            else:
                self.client.invoke(
                    GetMessagesViews(peer=self.client.resolve_peer(int(channel_link)), id=[int(post_id), ], increment=True))
            self.__disconnect()
            return True
        except:
            return False

    def send_comment(self, channel_link: str, post_id: int, comment_text):
        """Отправка комментария клиентом"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        try:
            self.join_channel(channel_link)
            self.__connect()
            if not channel_link.replace("-", "").isdigit():
                chat = self.client.get_chat(channel_link)
            m = self.client.get_discussion_message(int(chat.id), int(post_id))
            m.reply(comment_text)
            self.__disconnect()
            return True
        except:
            return False

    def click_button(self, channel_link: str, post_id: int, button_id: int):
        """Нажатие на кнопку клиентом"""
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        try:
            self.join_channel(channel_link)
            self.__connect()
            if not channel_link.replace("-", "").isdigit():
                chat = self.client.get_chat(channel_link)
            message = self.client.get_messages(chat.id, [int(post_id), ])[0]
            idx = 1
            for i in range(len(message.reply_markup)):
                for j in range(len(message.reply_markup[i])):
                    if idx == button_id:
                        self.client.request_callback_answer(
                            chat_id=message.chat.id,
                            message_id=message.id,
                            callback_data=message.reply_markup[i][j].callback_data
                        )
                        return True
                    idx += 1
            self.__disconnect()
            return False
        except:
            return False

    def get_last_messages(self, channel_link, count_messages: int):
        channel_link = channel_link.replace("https", "http").replace("http", "https").replace("+", "joinchat/")
        if not "joinchat/" in channel_link:
            channel_link = channel_link.replace("https://t.me/", "@")
        try:
            self.join_channel(channel_link)
            self.__connect()
            if not channel_link.replace("-", "").isdigit():
                chat = self.client.get_chat(channel_link)
            messages_result = []
            for message in self.client.get_chat_history(chat.id, limit=count_messages):
                messages_result.append(message)
            self.__disconnect()
            return messages_result
        except:
            return []
