import traceback

from telethon import events

from classes.UserList import UserList
from classes.Settings import settings
from keyboards.categories_inline import get_categories_keyboard
from keyboards.time_inline import get_time_keyboard
from loader import bot

users = UserList([])


@bot.on(events.CallbackQuery(pattern='Найти работу'))
async def button_request(event):
    try:
        user_info = await bot.get_entity(event.original_update.peer)
        user = users.get_user(user_info.id)
        await user.delete_last_msg()
        msg = await event.respond('Укажите категорию:',
                                  buttons=get_categories_keyboard(settings.categories))
        user.add_message(msg.id)
        await event.answer()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='Разместить вакансию'))
async def button_request(event):
    try:
        user_info = await bot.get_entity(event.original_update.peer)
        user = users.get_user(user_info.id)
        await user.delete_last_msg()
        msg = await event.respond(
            'Пожалуйста, оформите своё предложение по форме:\n#ищу\nТаргетолог/копирайтер/дизайнер и пр.\nЗадача:\nКраткое описание\nДля связи:\nВаш ник в телеграм')
        user.add_message(msg.id)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='category'))
async def button_request(event):
    try:
        category = int(event.data.decode('utf8').split(' ')[1])

        user_info = await bot.get_entity(event.original_update.peer)

        user = users.get_user(user_info.id)
        user.settings['category'] = category
        await user.delete_last_msg()
        msg = await event.respond('Укажите временной диапазон для поиска', buttons=get_time_keyboard(settings.time))
        user.add_message(msg.id)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


@bot.on(events.CallbackQuery(pattern='time'))
async def button_request(event):
    try:
        time = int(event.data.decode('utf8').split(' ')[1])

        user_info = await bot.get_entity(event.original_update.peer)

        user = users.get_user(user_info.id)

        user.settings['time'] = time
        await user.delete_last_msg()
        await user.get_paginate_messages()
        await user.show_results()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
