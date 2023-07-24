from flask import Flask
from flask import request

from database.interfaces import ChannelInterface
from database.interfaces import SubscriberInterface
from database.interfaces import ChannelReactionsInterface

from decorators.flask import is_logged_in_flask_decorator


def add_update_channel_emoji_percents(app: Flask):
    @app.route('/channels/update_channel_emoji_percents', methods=['POST'])
    @is_logged_in_flask_decorator
    def update_channel_emoji_percents():
        form_data = request.form
        channel_emoji_id = form_data.get("channel_emoji_id")
        emoji_percent_from = form_data.get("emoji_percent_from")
        emoji_percent_to = form_data.get("emoji_percent_to")
        ChannelReactionsInterface.update_model_by_id(int(channel_emoji_id), "subscribers_percent_from",
                                                     emoji_percent_from)
        ChannelReactionsInterface.update_model_by_id(int(channel_emoji_id), "subscribers_percent_to",
                                                     emoji_percent_to)
        return {'status': True, 'data': True}
