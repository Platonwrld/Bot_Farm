from math import ceil

from flask import Flask
from flask import request

from database.interfaces import ChannelInterface
from database.interfaces import SubscriberInterface

from decorators.flask import is_logged_in_flask_decorator


def add_get_pagination(app: Flask):
    @app.route('/channel/get_pagination', methods=['POST'])
    @is_logged_in_flask_decorator
    def channels_get_pagination():
        form_data = request.form
        if not form_data.get("page"):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        page = form_data.get('page')
        channels_models = ChannelInterface.get_pagination_by_(10, int(page))
        count_models = ChannelInterface.get_count_by_()
        channels_dicts = []
        for channel_model in channels_models:
            channel_dict = channel_model.to_dict()
            channel_dict.update({
                "count_subscribers": SubscriberInterface.get_count_by_channel_id(channel_model.id)
            })
            channels_dicts.append(channel_dict)
        return {'status': True, 'data': {
            "channels": channels_dicts,
            "count_pages": ceil(count_models / 10)
        }}
