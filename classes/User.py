import time

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
    # async def get_messages(self, channels):
    #     self.messages = await self.parser.get_messages_from_channels(channels)
    #     return []

    async def get_paginate_messages(self):
        amount = settings.pagination
        for channel in self.channels:
            try:
                print(channel)
                channel_messages = await self.parser.parse_channel(channel)
                self.messages.extend(channel_messages)
                self.parsed_channels.append(channel)
                if len(self.messages) > amount:
                    break
            except Exception:
                continue

        for channel in self.parsed_channels:
            self.channels.remove(channel)

        self.parsed_channels = []

    async def show_results(self):
        if self.loading:
            return
        else:
            self.loading = True

        amount = settings.pagination

        results = {
            'length': len(self.messages),
            'items': []
        }

        if results['length'] < amount:
            amount = len(self.messages)

        print(results['length'])

        for index in range(amount):
            elem = self.messages.pop(0)
            await bot.send_message(self.user_id, elem, buttons=get_return_keyboard(results['length']), parse_mode=html)

        if len(self.messages) <= amount:
            await self.get_paginate_messages()

        self.loading = False