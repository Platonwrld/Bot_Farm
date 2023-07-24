from flask import Flask
from flask import request

from database.interfaces import ProxyInterface
from database.interfaces import TgClientInterface



from decorators.flask import is_logged_in_flask_decorator

def add_delete(app: Flask):
    @app.route('/proxy/delete', methods=['POST'])
    @is_logged_in_flask_decorator
    def proxy_delete():
        form_data = request.form
        if not form_data.get('proxy_model_id'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        proxy_model_id = form_data.get('proxy_model_id')
        proxy = ProxyInterface.get_first_by_id(proxy_model_id)
        ProxyInterface.update_model_by_id(proxy.id, "is_active", False)
        proxy_tg_clients = TgClientInterface.get_all_by_proxy_id(proxy.id)
        for proxy_tg_client in proxy_tg_clients:
            new_proxy = ProxyInterface.get_random_active_proxy()
            TgClientInterface.update_model_by_id(proxy_tg_client.id, "proxy_id", new_proxy.id)
        delete_proxy_data = ProxyInterface.delete_model_by_id(
            proxy_model_id=proxy_model_id, )
        print(proxy_model_id)
        return {'status': True, 'data': delete_proxy_data}
