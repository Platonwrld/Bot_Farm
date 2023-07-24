from flask import Flask

from .admin import *
from .admin_login_session import *
from .channels import *
from .get_stats import add_get_stats
from .proxy import *
from .task import *
from .task_argument import *
from .tg_clients import *

from .get_is_null_notificated import add_get_is_null_notificated
from .set_is_null_notificated import add_set_is_null_notificated


def add_all_endpoints(app: Flask):
    add_admin_login_session_unauth(app)
    add_admin_auth(app)
    add_task_create(app)
    add_task_get_all(app)
    add_proxy_get_pagination(app)
    add_proxy_delete(app)
    add_proxy_create(app)
    add_task_argument_create(app)
    add_channel_create(app)
    add_channel_get_all(app)
    add_channel_get_pagination(app)
    add_channel_delete(app)
    add_tg_client_get_pagination(app)
    add_tg_client_delete(app)
    add_get_stats(app)
    add_task_delete(app)
    add_check_auth(app)
    add_get_is_null_notificated(app)
    add_set_is_null_notificated(app)
    add_task_get_current_sms_active(app)
    add_channel_get_one(app)
    add_update_channel_view_percents(app)
    add_update_channel_emoji_percents(app)
