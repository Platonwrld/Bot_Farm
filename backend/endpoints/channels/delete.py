from flask import Flask
from flask import request

from database.interfaces import ChannelInterface

from decorators.flask import is_logged_in_flask_decorator
def add_delete(app: Flask):
    @app.route('/channel/delete', methods=['POST'])
    @is_logged_in_flask_decorator
    def channels_delete():
        form_data = request.form
        if not form_data.get("channel_model_id"):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        channel_model_id = form_data.get('channel_model_id')
        delete_channel_model_data = ChannelInterface.delete_model_by_id(int(channel_model_id))
        return {'status': True, 'data': delete_channel_model_data}
