from datetime import datetime as dt
from functools import wraps

from flask import request

from database.interfaces import AdminLoginSessionInterface


def is_logged_in_flask_decorator(function):
    """Проверка запроса на авторизацию"""
    @wraps(function)
    def decorator_function(*args, **kwargs):
        form_data = request.form
        if not form_data.get('admin_login_session_model_session_hash'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}
        try:
            admin_login_session_model_session_hash = form_data.get('admin_login_session_model_session_hash')
            admin_login_session_model = AdminLoginSessionInterface.get_first_by_session_hash(
                admin_login_session_model_session_hash=admin_login_session_model_session_hash, )
            now = dt.utcnow()
            if admin_login_session_model:
                flask_session_is_not_end = admin_login_session_model.end_date > now
                if not (flask_session_is_not_end):
                    return {'status': False, 'error': 'Вы не авторизованы'}
            else:
                return {'status': False, 'error': 'Вы не авторизованы'}
        except:
            return {'status': False, 'error': 'Вы не авторизованы'}
        return function()

    return decorator_function
