import traceback

from telethon import events

from classes.Settings import settings
from filters import userFilter
from keyboards.welcome_inline import welcome_keyboard
from loader import bot


@bot.on(events.NewMessage(pattern='/update'))
async def start(event):
    try:
        settings.update()
        await event.respond('Настройки обновлены')
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(func=userFilter, pattern='/start'))
async def start(event):
    try:
        await event.respond('Добро пожаловать!',
                            buttons=welcome_keyboard)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
