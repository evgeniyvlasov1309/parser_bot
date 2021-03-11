from classes.Settings import settings
from loader import bot


async def send_message_to_admins(message):
    for admin in settings.admins:
        await bot.send_message(admin, message)


def get_loading_message(num):
    new_array = []
    for item in range(num):
        new_array.append('.')

    return f"Ищем вакансии...{''.join(new_array)}"
