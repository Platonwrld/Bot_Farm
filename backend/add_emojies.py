from database.interfaces import ChannelReactionsInterface
from app_init import get_settings

config = get_settings()
for emoji in config['default_emojis']:
    ChannelReactionsInterface.create_model(2, emoji)