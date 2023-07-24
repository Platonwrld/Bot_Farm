from functools import wraps

from flask import request

from database.interfaces import AdminInterface


def is_password_valid_flask_decorator(function):
    """Валидация пароля"""
    @wraps(function)
    def decorator_function(*args, **kwargs):
        form_data = request.form
        if not form_data.get('username') or not form_data.get('password'):
            return {'status': False, 'error': 'Получены не все необходимые данные'}

        admin_model_username = form_data.get('username')
        admin_model_password = form_data.get('password')
        admin_model = AdminInterface.get_first_by_username(
            admin_model_username=admin_model_username, )
        check_admin_data = AdminInterface.check_password(
            admin_model_id=admin_model.id, admin_model_password=admin_model_password, )
        if not (check_admin_data):
            return {'status': False, 'error': 'Введен не верный пароль'}
        return function()

    return decorator_function
