import os

from database.interfaces import TgClientInterface
from telegram_model import TelegramMyClient




count_checked = 2135
count_banned = 1182
clients = TgClientInterface.get_all_by_()[count_checked:]
for client in clients:
    client = TelegramMyClient(client.phone_number)
    # count_checked += 1
    # if client.check_account_is_banned():
    #     count_banned += 1
    #     TgClientInterface.delete_model_by_id(client.tg_client_settings.id)
    # os.system("clear")
    # print(f"Count checked: {count_checked}")
    # print(f"Count banned: {count_banned}")
    # print(f"Persent banned: {round(count_banned / (count_checked / 100), 2)}%")