import traceback

from telethon import events
from telethon.extensions import html

from classes.UserList import UserList
from classes.Settings import settings
from classes.User import User
from keyboards.categories_inline import get_categories_keyboard
from keyboards.return_keyboard import get_return_keyboard
from keyboards.time_inline import get_time_keyboard
from loader import bot

users = UserList([])


@bot.on(events.CallbackQuery(pattern='Найти работу'))
async def button_request(event):
    try:
        await event.respond('Укажите категорию:',
                            buttons=get_categories_keyboard(settings.categories))
        await event.answer()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='Разместить вакансию'))
async def button_request(event):
    try:
        await event.respond(
            'Пожалуйста, оформите своё предложение по форме:\n#ищу\nТаргетолог/копирайтер/дизайнер и пр.\nЗадача:\nКраткое описание\nДля связи:\nВаш ник в телеграм')
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='category'))
async def button_request(event):
    try:
        category = int(event.data.decode('utf8').split(' ')[1])

        user_info = await bot.get_entity(event.original_update.peer)

        user = User(user_info.id, user_info.username, category, '')

        users.add_user(user)
        await event.respond('Укажите временной диапазон для поиска', buttons=get_time_keyboard(settings.time))
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='time'))
async def button_request(event):
    try:
        time = int(event.data.decode('utf8').split(' ')[1])

        user_info = await bot.get_entity(event.original_update.peer)

        user = users.get_user(user_info.id)
        user.settings['time'] = time
        results = await user.show_results()
        results_len = results['length']
        await event.respond(f'Найдено {results_len}', buttons=get_return_keyboard(results_len))
        for msg in results['items']:
            await event.respond(msg, parse_mode=html)

        await event.answer()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
