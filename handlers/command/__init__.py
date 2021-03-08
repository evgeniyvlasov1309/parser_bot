import traceback

from telethon import events

from classes.Settings import settings
from classes.User import User
from filters import userFilter
from handlers.inline_buttons import users
from keyboards.welcome_inline import welcome_keyboard
from loader import bot


@bot.on(events.NewMessage(pattern='/update'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = users.get_user(user_info.id)
        settings.update()
        user.add_message(event.message.id)
        msg = await event.respond('Настройки обновлены')
        user.add_message(msg.id)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(func=userFilter, pattern='/start'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = User(user_info.id, user_info.username, '', '')
        users.add_user(user)
        msg = await event.respond('Добро пожаловать!',
                                  buttons=welcome_keyboard)
        user.add_message(msg.id)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
