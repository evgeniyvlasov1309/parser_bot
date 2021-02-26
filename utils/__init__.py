from classes.Settings import settings
from loader import bot


async def send_message_to_admins(message):
    for admin in settings.admins:
        await bot.send_message(admin, message)
