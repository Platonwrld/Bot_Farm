from flask import Flask
from flask import request

from database.interfaces import TgClientInterface


from decorators.flask import is_logged_in_flask_decorator

def add_delete(app: Flask):
    @app.route('/tg_client/delete', methods=['POST'])
    @is_logged_in_flask_decorator
    def tg_client_delete():
        form_data = request.form
        if not form_data.get("tg_client_model_id"):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        tg_client_model_id = form_data.get('tg_client_model_id')
        delete_tg_clients_model_data = TgClientInterface.delete_model_by_id(int(tg_client_model_id))
        return {'status': True, 'data': delete_tg_clients_model_data}
