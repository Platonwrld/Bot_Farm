from math import ceil

from flask import Flask
from flask import request

from database.interfaces import ProxyInterface
from database.interfaces import TgClientInterface

from decorators.flask import is_logged_in_flask_decorator

def add_get_pagination(app: Flask):
    @app.route('/proxy/get_pagination', methods=['POST'])
    @is_logged_in_flask_decorator
    def proxy_get_pagination():
        form_data = request.form
        if not form_data.get('page'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        page = form_data.get('page')
        proxies_models = ProxyInterface.get_pagination_by_(10, int(page))
        proxies = []
        for proxy_model in proxies_models:
            proxy_model_dict = proxy_model.to_dict()
            proxy_model_dict.update({
                "count_accounts": TgClientInterface.get_count_by_proxy(proxy_model.id)
            })
            proxies.append(proxy_model_dict)
        models_count = ProxyInterface.get_count_by_()
        return {
            "status": True,
            "data": {
                "proxies": proxies,
                "count_pages": ceil(models_count / 10)
            }
        }
