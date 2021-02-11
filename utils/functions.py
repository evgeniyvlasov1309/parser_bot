import datetime

from telethon.extensions import html
from telethon.tl.types import PeerChannel

from data import config
from loader import client, bot


async def get_messages_from_channels(channels, key_word):
    all_messages = []
    for channel in channels:
        channel_entity = await client.get_entity(channel)
        messages = await dump_all_messages(channel_entity, key_word)
        all_messages.extend(messages)
    return all_messages


async def dump_all_messages(channel, key_word):
    offset_date = datetime.datetime(2021, 2, 4, tzinfo=datetime.timezone.utc)
    all_messages = []

    async for message in client.iter_messages(channel, search=key_word):
        if offset_date < message.date:
            all_messages.append(message)
        else:
            break

    return all_messages


async def send_messages(event, text, sender):
    messages = await get_messages_from_channels(config.CHANNELS, text)
    messages_total = len(messages)
    if messages_total:
        await event.respond(f'Найдено: {messages_total}')
        for message in messages:
            message_sender = message.from_id
            if isinstance(message_sender, PeerChannel):
                instance = await client.get_entity(message_sender.channel_id)
            else:
                instance = await client.get_entity(message_sender.user_id)
            name = instance.username
            message_text = f'Автор: <a href=\'https://t.me/{name}\'>{name}<a/>\nОпубликовано: {message.date.date()}\n\n' + message.text
            await bot.send_message(sender, message_text, parse_mode=html)
    else:
        await event.respond('К сожалению, по заданному ключевому слову ничего не найдено')
