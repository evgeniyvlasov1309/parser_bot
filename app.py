from telethon import events, Button

from data import config
from keyboards.inline import category_keyboard
from loader import client, bot
from utils.functions import get_messages_from_channels


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await bot.send_message(event.peer_id,
                           'Добро пожаловать!\n\nВведите ключевое слово для поиска вакансий, либо укажите категорию:',
                           buttons=category_keyboard)
    raise events.StopPropagation


@bot.on(events.CallbackQuery())
async def button_request(event):
    text = event.data.decode('utf8')
    await event.respond(f'Получено сообщение: {text}')
    # messages = await get_messages_from_channels(config.CHANNELS, text)
    # messages_total = len(messages)
    # if messages_total:
    #     await event.respond(f'Найдено: {messages_total}')
    #     for message in messages:
    #         bot.send_message(event.peer_id, message)
    # else:
    #     await event.respond('К сожалению, по заданному ключевому слову ничего не найдено')
    await event.answer()


@bot.on(events.NewMessage())
async def echo(event):
    await event.respond(f'Получено сообщение: {event.text}')
    # messages = await get_messages_from_channels(config.CHANNELS, event.text)
    # messages_total = len(messages)
    # if messages_total:
    #     await event.respond(f'Найдено: {messages_total}')
    #     for message in messages:
    #         bot.send_message(event.peer_id, message)
    # else:
    #     await event.respond('К сожалению, по заданному ключевому слову ничего не найдено')


# async def main():
#     await get_messages_from_channels(config.CHANNELS, 'frontend')


if __name__ == '__main__':
    client.run_until_disconnected()
    # client.loop.run_until_complete(main())
