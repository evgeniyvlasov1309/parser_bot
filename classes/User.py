from classes.Parser import Parser
from classes.Settings import settings


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

    # async def get_messages(self, channels):
    #     self.messages = await self.parser.get_messages_from_channels(channels)
    #     return []

    async def get_paginate_messages(self):
        amount = settings.pagination
        for channel in self.channels:
            try:
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
        amount = settings.pagination

        if len(self.messages) <= amount:
            await self.get_paginate_messages()

        results = {
            'length': len(self.messages),
            'items': []
        }

        if results['length'] < amount:
            amount = len(self.messages)

        for index in range(amount):
            elem = self.messages.pop(0)
            results['items'].append(elem)

        return results
