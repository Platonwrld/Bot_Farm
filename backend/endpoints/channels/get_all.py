from flask import Flask
from flask import request

from database.interfaces import ChannelInterface
from database.interfaces import SubscriberInterface

from decorators.flask import is_logged_in_flask_decorator


def add_get_all(app: Flask):
    @app.route('/channels/get_all', methods=['POST'])
    @is_logged_in_flask_decorator
    def channels_get_all():
        form_data = request.form
        channels_models = ChannelInterface.get_all_by_()
        channels_dicts = []
        for channel_model in channels_models:
            channel_dict = channel_model.to_dict()
            channel_dict.update({
                "count_subscribers": SubscriberInterface.get_count_by_channel_id(channel_model.id)
            })
            channels_dicts.append(channel_dict)
        return {'status': True, 'data': channels_dicts}
