from flask import Flask
from flask import request

from database.interfaces import AdminLoginSessionInterface

from decorators.flask import is_logged_in_flask_decorator


def add_unauth(app: Flask):
    @app.route('/admin_login_session/unauth', methods=['POST'])
    @is_logged_in_flask_decorator
    def admin_login_session_unauth():
        form_data = request.form
        if not form_data.get('admin_login_session_model_session_hash'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        admin_login_session_model_session_hash = form_data.get('admin_login_session_model_session_hash')
        admin_login_session_model = AdminLoginSessionInterface.get_first_by_session_hash(
            admin_login_session_model_session_hash=admin_login_session_model_session_hash, )
        delete_admin_login_session_data = AdminLoginSessionInterface.delete_model_by_id(
            admin_login_session_model_id=admin_login_session_model.id, )
        return {'status': True, 'data': delete_admin_login_session_data}
