import traceback

from telethon import events, Button
from classes.User import User
from handlers.inline_buttons import users
from keyboards.return_keyboard import get_return_keyboard
from keyboards.welcome_inline import welcome_keyboard
from loader import bot
from utils import send_message_to_admins
from variables.texts import welcome_text


@bot.on(events.NewMessage(pattern='Вернуться в начало'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = users.get_user(user_info.id)
        msg = await event.respond('Возвращаемся в начало', buttons=Button.clear())
        user.add_message(msg)
        user.add_user_message(event.message.id)
        await user.delete_all_messages()
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = User(user_info.id, user_info.username, '', '')
        users.add_user(user)
        msg = await event.respond(welcome_text,
                                  buttons=welcome_keyboard)
        user.add_message(msg)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(pattern='#ищу'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = users.get_user(user_info.id)
        user.add_user_message(event.message.id)
        await user.delete_last_msg()
        await send_message_to_admins(event.text)
        msg = await event.respond('Вакансия отправлена на модерацию', buttons=get_return_keyboard(0))
        user.add_message(msg)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(pattern='Показать еще'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id)
        user = users.get_user(user_info.id)
        user.add_user_message(event.message.id)
        await user.show_results()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
