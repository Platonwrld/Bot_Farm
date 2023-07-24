from .admin import *
from .admin_login_session import *
from .channel import *
from .device import *
from .proxy import *
from .subscriber import *
from .task import *
from .task_argument import *
from .task_make import *
from .tg_app import *
from .tg_client import *
from .u_name import *
from .nicknames import *
from .avatars import *
from .bios import *
from .channel_reactions import *
from .tasks_for_make import *

models = [AdminModel, AdminLoginSessionModel, ChannelModel, ProxyModel, TgAppModel, DeviceModel, UNameModel,
          TgClientModel, TaskModel, TaskArgumentModel, TaskMakeModel, SubscriberModel, NicknameModel, AvatarModel,
          BioModel,
          ChannelReactionsModel,
          TaskForMakeModel
]
