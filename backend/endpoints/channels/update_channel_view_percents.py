from flask import Flask
from flask import request

from database.interfaces import ChannelInterface
from database.interfaces import SubscriberInterface
from database.interfaces import ChannelReactionsInterface

from decorators.flask import is_logged_in_flask_decorator


def add_update_channel_view_percents(app: Flask):
    @app.route('/channels/update_channel_view_percents', methods=['POST'])
    @is_logged_in_flask_decorator
    def update_channel_view_percents():
        form_data = request.form
        channel_id = form_data.get("channel_id")
        view_percent_from = form_data.get("view_percent_from")
        view_percent_to = form_data.get("view_percent_to")
        ChannelInterface.update_model_by_id(int(channel_id), "view_percent_from", view_percent_from)
        ChannelInterface.update_model_by_id(int(channel_id), "view_percent_to", view_percent_to)
        channel_model = ChannelInterface.get_first_by_id(int(channel_id))
        channel_dict = channel_model.to_dict()
        channel_dict.update({
            "count_subscribers": SubscriberInterface.get_count_by_channel_id(channel_model.id)
        })
        channel_reactions = ChannelReactionsInterface.get_channel_emojis(channel_model.id)
        channel_reactions_list = []
        for channel_reaction in channel_reactions:
            channel_reactions_list.append(channel_reaction.to_dict())
        channel_dict.update({
            "channel_reactions": channel_reactions_list
        })
        return {'status': True, 'data': channel_dict}
