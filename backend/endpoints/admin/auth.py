from datetime import datetime as dt
from datetime import timedelta as td

from flask import Flask
from flask import request

from database.interfaces import AdminInterface
from database.interfaces import AdminLoginSessionInterface
from decorators.flask import is_password_valid_flask_decorator

from random import choices
from string import ascii_letters


def add_auth(app: Flask):
    @app.route('/admin/auth', methods=['POST'])
    @is_password_valid_flask_decorator
    def admin_auth():
        form_data = request.form
        if not form_data.get('username'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        admin_model_username = form_data.get('username')
        admin_login_session_model_session_hash = ''.join(choices(ascii_letters, k=10))
        now = dt.utcnow()
        one_day = td(days=1)
        admin_login_session_model_end_date = now + one_day
        admin_model = AdminInterface.get_first_by_username(
            admin_model_username=admin_model_username, )
        admin_model_id = AdminLoginSessionInterface.create_model(
            admin_login_session_model_admin_id=admin_model.id,
            admin_login_session_model_session_hash=admin_login_session_model_session_hash,
            admin_login_session_model_end_date=admin_login_session_model_end_date, )
        create_admin_login_session_data = AdminLoginSessionInterface.get_first_by_id(admin_model_id).to_dict()
        return {'status': True, 'data': admin_login_session_model_session_hash}
