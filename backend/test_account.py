from telegram_model import TelegramMyClient
from database.interfaces import TgClientInterface
from random import choice

client_number = choice(TgClientInterface.get_all_by_())

client = TelegramMyClient(client_number.phone_number)
client.send_message("@ether182", "TEST")
