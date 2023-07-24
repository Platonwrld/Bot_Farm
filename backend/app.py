from app_init import get_settings
from app_init import flask_app as app
from endpoints import add_all_endpoints

# Запуск Bakcend эндпоинтов Flask
add_all_endpoints(app)


@app.route("/")
def start():
    return "RUNNED API V2.02 VERSION"


if __name__ == '__main__':
    app.run(debug=get_settings()['flask']['debug'], port=get_settings()['flask']['port'],
            host=('0.0.0.0' if get_settings()['flask']['is_public_host'] else None))
