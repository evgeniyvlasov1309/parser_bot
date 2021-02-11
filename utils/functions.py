import datetime

from loader import client


async def get_messages_from_channels(channels, key_word):
    all_messages = []
    for channel in channels:
        channel_entity = await client.get_entity(channel)
        messages = await dump_all_messages(channel_entity, key_word)
        all_messages.extend(messages)
    return all_messages


async def dump_all_messages(channel, key_word):
    offset_date = datetime.datetime(2021, 2, 1, tzinfo=datetime.timezone.utc)
    all_messages = []

    async for message in client.iter_messages(channel, search=key_word):
        if offset_date < message.date:
            all_messages.append(message)
        else:
            break

    return all_messages
