from pyrogram import Client
from database.interfaces import SubscriberInterface
from database.interfaces import TgClientInterface
from database.interfaces import ChannelInterface
from database.interfaces import ChannelReactionsInterface
from random import uniform, randint
from pyrogram.filters import channel
from datetime import datetime as dt
from datetime import timedelta as td
from app_init import tg_bot
from threading import Thread
from database.interfaces import TaskForMakeInterface

with open("checker.txt", 'r') as file:
    session_string = file.read()
client = Client("checker", 8, "", session_string=session_string, in_memory=True)


@client.on_message(filters=channel)
def on_message(client, message):
    def start_channel(message):
        def start_views(active_percent, subscribers, days):
            views_count = int(len(subscribers) / 100 * active_percent)
            views_subscribers = subscribers[:views_count + 1]
            tg_bot.send_message(5951391062, f"VIEW {len(views_subscribers)}")
            for subscriber in views_subscribers:
                timer = 60 * randint(1, 360) + (days * 24 * 60 * 60)
                tg_client = TgClientInterface.get_first_by_id(subscriber.tg_client_id)
                TaskForMakeInterface.create_model("make_view_task", (
                        0,
                        tg_client.phone_number,
                        str(message.chat.id),
                        message.id
                    ), dt.utcnow() + td(seconds=timer))
        print(f"START VIEW {message.chat.id}")
        channel_model = ChannelInterface.get_first_by_channel_id(message.chat.id)
        subscribers = SubscriberInterface.get_all_by_channel_id(channel_model.id)
        channel_reactions_models = ChannelReactionsInterface.get_channel_emojis(channel_model.id)
        percent = round(uniform(channel_model.view_percent_from, channel_model.view_percent_to), 2)
        days = 0
        while percent != 0:
            if percent > 100:
                active_percent = 100
            else:
                active_percent = percent
            Thread(target=start_views, args=(active_percent, subscribers, days, )).start()
            days += 1
            percent -= active_percent
        counter = 0

        for channel_reaction_model in channel_reactions_models:
            reaction_percent = uniform(channel_reaction_model.subscribers_percent_from,
                                       channel_reaction_model.subscribers_percent_to)
            reaction_count = int(len(subscribers) / 100 * reaction_percent)
            if reaction_count:
                reactions_subscribers = subscribers[counter:reaction_count + counter + 1]
                tg_bot.send_message(5951391062, f"REACTION {channel_reaction_model.emoji_type} {reaction_count}")
                for subscriber in reactions_subscribers:
                    timer = 60 * randint(1, 360)
                    tg_client = TgClientInterface.get_first_by_id(subscriber.tg_client_id)
                    TaskForMakeInterface.create_model("make_reaction_task", (
                            0,
                            tg_client.phone_number,
                            str(message.chat.id),
                            message.id,
                            channel_reaction_model.emoji_type
                        ), dt.utcnow() + td(seconds=timer))
                counter += reaction_count
    Thread(target=start_channel, args=(message, )).start()
client.run()
