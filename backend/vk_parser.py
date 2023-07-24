import json

import requests
from bs4 import BeautifulSoup
from app_init import get_vk_api
from time import sleep
from database.interfaces import AvatarInterface
from database.interfaces import BioInterface
from database.interfaces import NicknameInterface
from threading import Thread


def get_user_followers(username, offset):
    """Функция для получения списка подписчиков пользователя пагинация"""
    vk = get_vk_api()
    user_id = vk.users.get(user_ids=username)[0]['id']
    followers = vk.friends.get(user_id=user_id, offset=offset, fields="photo_max, status, domain, sex, nickname")
    return followers


def get_all_user_followers(username):
    """Получение всех подписчиков пользователя"""
    counter = 0
    while True:
        followers_result = get_user_followers(username, counter)
        counter += len(followers_result['items'])
        if followers_result['count'] - 200 <= counter:
            break
        for follower in followers_result['items']:
            Thread(target=parse_follower, args=(follower, )).start()
        sleep(10)


def get_group_followers(username, offset):
    """Получение списка подписчиков группы пагинация"""
    print("GET FOLLOWERS")
    vk = get_vk_api()
    group_id = vk.groups.getById(group_id=username)[0]['id']
    followers = \
        vk.groups.getMembers(group_id=group_id, offset=offset, count=1000,
                             fields="photo_max, status, domain, sex, nickname")
    return followers


def get_all_group_followers(username):
    """Получение всех подписчиков группы"""
    counter = 0
    while True:
        followers_result = get_group_followers(username, counter)
        counter += len(followers_result['items'])
        print(counter)
        if followers_result['count'] - 200 <= counter:
            break
        for follower in followers_result['items']:
            Thread(target=parse_follower, args=(follower, )).start()
        sleep(10)


def parse_follower(follower):
    """Распаршивание модели пользователя"""
    is_male = follower.get("sex") == 2
    if follower.get("photo_max"):
        if not "camera_" in follower.get("photo_max"):
            if not AvatarInterface.check_is_exists_by_download_href(follower.get("photo_max")):
                AvatarInterface.create_avatar(follower.get("photo_max"), is_male)
    if follower.get("status"):
        if not BioInterface.check_bio_is_exists(follower.get("status")):
            BioInterface.create_bio(follower.get("status"), is_male)
    if not "id" in follower.get("domain").replace('.', ""):
        if not check_tg_login(follower.get("domain")):
            if not follower.get("nickname"):
                if not NicknameInterface.check_model_is_exists(follower['first_name'], follower['last_name'],
                                                               follower['domain'].replace('.', "")):
                    NicknameInterface.create_nickname(follower['first_name'], follower['last_name'],
                                                      follower['domain'].replace('.', ""),
                                                      is_male)
            else:
                if not NicknameInterface.check_model_is_exists(follower['nickname'], "",
                                                               follower['domain'].replace('.', "")):
                    NicknameInterface.create_nickname(follower['nickname'], "",
                                                      follower['domain'].replace('.', ""),
                                                      is_male)


def check_tg_login(username):
    """Проверка логина Telegram на уникальность"""
    response = requests.get(f"https://t.me/{username}")
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.find("div", {"class": "tgme_page_title"})
    if title is None:
        return False
    return True

