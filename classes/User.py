from telethon import Button
from telethon.extensions import html

from classes.Parser import Parser
from classes.Settings import settings
from keyboards.return_keyboard import get_return_keyboard
from loader import bot


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
        self.loading = False

    def remove_parsed_channels(self):
        for channel in self.parsed_channels:
            self.channels.remove(channel)

        self.parsed_channels = []

    async def get_paginate_messages(self):
        amount = settings.pagination

        if len(self.channels) > 0:
            await bot.send_message(self.user_id, 'Ищем вакансии...', buttons=Button.clear())

        for channel in self.channels:
            try:
                channel_messages = await self.parser.parse_channel(channel)
                self.messages.extend(channel_messages)
                self.parsed_channels.append(channel)
                if len(self.messages) > amount:
                    break
            except Exception:
                continue

        messages_len = len(self.messages)
        await bot.send_message(self.user_id, 'Поиск завершен', buttons=get_return_keyboard(messages_len))
        self.remove_parsed_channels()

    async def send_messages(self):
        for index in range(settings.pagination):
            elem = self.messages.pop(0)
            await bot.send_message(self.user_id, elem, parse_mode=html)

    async def show_results(self):
        if self.loading:
            return
        else:
            self.loading = True

        await self.send_messages()

        if len(self.messages) <= settings.pagination:
            await self.get_paginate_messages()

        self.loading = False
