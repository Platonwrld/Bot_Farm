import json

from flask import Flask
from flask import request

from database.interfaces import ChannelInterface
from database.interfaces import TgClientInterface
from telegram_model import TelegramMyClient
from app_init import get_settings

from decorators.flask import is_logged_in_flask_decorator
def add_create(app: Flask):
    @app.route('/channels/create', methods=['POST'])
    @is_logged_in_flask_decorator
    def channels_create():
        form_data = request.form
        if not form_data.get('channel_link'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        channel_link = form_data.get("channel_link")
        is_seen_active = True
        tg_model = TgClientInterface.get_first_by_id(get_settings()['service_tg_account_id'])
        tg_client = TelegramMyClient(tg_model.phone_number)
        channel_data = tg_client.get_channel_data(channel_link)
        if channel_data:
            create_channel_data = ChannelInterface.create_model(
                channel_model_channel_id=channel_data.id,
                channel_model_channel_name=channel_data.title,
                channel_model_channel_invite_link=channel_link,
                channel_model_is_seen_active=is_seen_active
            )
            channel_data = ChannelInterface.get_first_by_id(create_channel_data)
            return {'status': True, 'data': channel_data.to_dict()}
        return {
            "status": False,
            "error": "Попытка добавления несвущетствующего канала"
        }
