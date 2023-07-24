from flask import Flask
from decorators.flask import is_logged_in_flask_decorator


def add_check_auth(app: Flask):
    @app.route('/admin/check_auth', methods=['POST'])
    @is_logged_in_flask_decorator
    def admin_check_auth():
        return {
            "status": True
        }
