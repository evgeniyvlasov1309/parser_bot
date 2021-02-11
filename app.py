import traceback
import datetime

from telethon import events

from keyboards.inline import category_keyboard
from loader import client, bot
from utils.functions import send_messages


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await bot.send_message(event.peer_id,
                           'Добро пожаловать!\n\nВведите ключевое слово для поиска вакансий, либо укажите категорию:',
                           buttons=category_keyboard)
    raise events.StopPropagation


@bot.on(events.CallbackQuery())
async def button_request(event):
    try:
        text = event.data.decode('utf8')
        sender = event.original_update.peer
        await send_messages(event, text, sender)
        await event.answer()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage())
async def echo(event):
    try:
        sender = event.peer_id
        await send_messages(event, event.text, sender)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


if __name__ == '__main__':
    client.run_until_disconnected()
