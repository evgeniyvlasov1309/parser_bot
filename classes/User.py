from telethon import Button
from telethon.extensions import html

from classes.Parser import Parser
from classes.Settings import settings
from keyboards.return_keyboard import get_return_keyboard
from loader import bot
from utils import get_loading_message


class User:
    def __init__(self, user_id, username, active_category, active_time):
        self.user_id = user_id
        self.username = username
        self.settings = {
            'category': active_category,
            'time': active_time,
        }
        self.channels = settings.channels.copy()
        self.parsed_channels = []
        self.parser = Parser(self.settings)
        self.messages = []
        self.messages_ids = []
        self.user_messages_ids = []

    def add_message(self, id):
        self.messages_ids.append(id)

    def add_user_message(self, id):
        self.user_messages_ids.append(id)

    async def delete_all_messages(self):
        array = []
        array.extend(self.messages_ids)
        array.extend(self.user_messages_ids)
        await bot.delete_messages(self.user_id, array)

    async def delete_last_msg(self):
        last_index = len(self.messages_ids)
        last_elem = self.messages_ids.pop(last_index - 1)
        await bot.delete_messages(self.user_id, last_elem)

    def remove_parsed_channels(self):
        for channel in self.parsed_channels:
            self.channels.remove(channel)

        self.parsed_channels = []

    async def get_paginate_messages(self):
        amount = settings.pagination
        loading_msg = ''

        if len(self.channels) > 0:
            loading_msg = await bot.send_message(self.user_id, 'Ищем вакансии...', buttons=Button.clear())
            self.add_message(loading_msg.id)
            await self.delete_last_msg()

            loading_msg = await bot.send_message(self.user_id, 'Ищем вакансии...')
            self.add_message(loading_msg.id)

        for (index, channel) in enumerate(self.channels):
            try:
                channel_messages = await self.parser.parse_channel(channel)
                self.messages.extend(channel_messages)
                self.parsed_channels.append(channel)
                await bot.edit_message(self.user_id, loading_msg, get_loading_message(index))
                if len(self.messages) > amount:
                    break
            except Exception:
                continue

        messages_len = len(self.messages)
        complete_msg = await bot.send_message(self.user_id, 'Поиск завершен', buttons=get_return_keyboard(messages_len))
        self.add_message(complete_msg.id)
        self.remove_parsed_channels()

    async def send_messages(self):
        for index in range(settings.pagination):
            elem = self.messages.pop(0)
            msg = await bot.send_message(self.user_id, elem, parse_mode=html)
            self.add_message(msg.id)

    async def show_results(self):
        await self.send_messages()

        if len(self.messages) <= settings.pagination:
            await self.get_paginate_messages()
