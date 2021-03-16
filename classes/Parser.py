from datetime import datetime, timedelta

from classes.Settings import settings
from loader import client


class Parser:
    def __init__(self, user_settings):
        self.all_messages = []
        self.settings = user_settings

    async def get_messages_from_channels(self, channels):
        messages = []
        for channel in channels:
            try:
                channel_messages = await self.parse_channel(channel)
                messages.extend(channel_messages)
            except Exception:
                continue

        return messages

    async def parse_channel(self, channel):
        messages = []
        async for message in client.iter_messages(channel):
            filter_result = self.filter_message(message)
            if filter_result == 'too old':
                break
            elif filter_result == 'ok':
                self.all_messages.append(message)
                modified_msg = await self.set_message_link(message)
                messages.append(modified_msg)

        return messages

    async def set_message_link(self, message):
        channel_id = message.peer_id.channel_id
        channel = await client.get_entity(channel_id)
        message_link = f'{channel.username}/{message.id}'
        message_text = f'Ссылка: <a href=\'https://t.me/{message_link}\'>https://t.me/{message_link}<a/>\n\n' + message.text
        return message_text

    def filter_message(self, message):
        time_index = self.settings['time']
        delta_time = int(settings.time[time_index]['value'])
        offset_date = datetime.utcnow() - timedelta(hours=delta_time)
        md = message.date
        native_md = md.replace(tzinfo=None)
        if offset_date > native_md:
            return 'too old'

        for msg in self.all_messages:
            if msg.raw_text == message.raw_text:
                return 'fail'

        category_index = self.settings['category']

        hashtags = settings.categories[category_index]['hashtags']

        is_has_hashtag = False

        for hashtag in hashtags:
            if hashtag == '':
                return
            if message.raw_text.find(hashtag) != -1:
                is_has_hashtag = True

        keywords = settings.categories[category_index]['keywords']

        is_has_keywords = False

        for keyword in keywords:
            if keyword == '':
                return
            if message.raw_text.find(keyword) != -1:
                is_has_keywords = True

        if is_has_hashtag and is_has_keywords:
            return 'ok'
        else:
            return 'fail'
