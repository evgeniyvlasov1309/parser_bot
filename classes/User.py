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
        self.parser = Parser(self.settings)
        self.messages = []

    async def get_messages(self):
        self.messages = await self.parser.get_messages_from_channels(settings.channels)

    async def show_results(self):
        amount = settings.pagination

        if len(self.messages) == 0:
            await self.get_messages()

        results = {
            'length': len(self.messages),
            'items': []
        }

        if len(self.messages) < settings.pagination:
            amount = len(self.messages)

        for index in range(amount):
            elem = self.messages.pop(0)
            results['items'].append(elem)

        return results
