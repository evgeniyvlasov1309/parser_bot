import traceback

from telethon import events
from telethon.extensions import html

from classes.Settings import settings
from handlers.inline_buttons import users
from keyboards.return_keyboard import get_return_keyboard
from keyboards.welcome_inline import welcome_keyboard
from loader import bot


@bot.on(events.NewMessage(pattern='Вернуться в начало'))
async def start(event):
    try:
        await event.respond('Добро пожаловать!',
                            buttons=welcome_keyboard)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(pattern='#ищу'))
async def start(event):
    try:
        for admin in settings.admins:
            await bot.send_message(admin, event.text)
        await event.respond('Вакансия отправлена на модерацию')
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.NewMessage(pattern='Показать еще'))
async def start(event):
    try:
        user_info = await bot.get_entity(event.original_update.message.peer_id.user_id)
        user = users.get_user(user_info.id)
        results = await user.show_results()
        results_len = results['length']
        for msg in results['items']:
            await event.respond(msg, buttons=get_return_keyboard(results_len), parse_mode=html)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())