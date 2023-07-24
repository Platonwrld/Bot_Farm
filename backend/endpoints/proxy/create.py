from flask import Flask
from flask import request

from database.interfaces import ProxyInterface

from decorators.flask import is_logged_in_flask_decorator


def add_create(app: Flask):
    @app.route('/proxy/create', methods=['POST'])
    @is_logged_in_flask_decorator
    def proxy_create():
        form_data = request.form
        if not form_data.get('proxy_model_type') or not form_data.get('proxy_model_ip') or not form_data.get(
                'proxy_model_port'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        proxy_model_type = form_data.get('proxy_model_type')
        proxy_model_ip = form_data.get('proxy_model_ip')
        proxy_model_port = form_data.get('proxy_model_port')
        proxy_model_username = form_data.get('proxy_model_username')
        proxy_model_password = form_data.get('proxy_model_password')
        create_proxy_data = ProxyInterface.create_model(
            proxy_model_type=proxy_model_type, proxy_model_ip=proxy_model_ip, proxy_model_username=proxy_model_username,
            proxy_model_password=proxy_model_password, proxy_model_port=proxy_model_port, )
        return {'status': True, 'data': create_proxy_data}
