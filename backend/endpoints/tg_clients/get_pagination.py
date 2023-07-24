from math import ceil

from flask import Flask
from flask import request

from database.interfaces import TgClientInterface

from decorators.flask import is_logged_in_flask_decorator


def add_get_pagination(app: Flask):
    @app.route('/tg_client/get_pagination', methods=['POST'])
    @is_logged_in_flask_decorator
    def tg_clients_get_pagination():
        form_data = request.form
        if not form_data.get('page'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        page = form_data.get('page')
        tg_clients_models = TgClientInterface.get_pagination_by_(10, int(page))
        tg_clients = []
        for tg_clients_model in tg_clients_models:
            tg_clients_model_dict = tg_clients_model.to_dict()
            tg_clients.append(tg_clients_model_dict)
        models_count = TgClientInterface.get_count_by_()
        return {
            "status": True,
            "data": {
                "tg_clients": tg_clients,
                "count_pages": ceil(models_count / 10)
            }
        }
