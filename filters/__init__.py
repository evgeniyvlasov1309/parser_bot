from datetime import datetime

from classes.Settings import settings
from loader import bot


def isAdmin(username):
    for admin in settings.admins:
        if admin == username:
            return True
    return False

async def userFilter(event):
    access = False
    user = await bot.get_entity(event.message.peer_id)

    if isAdmin(user.username):
        return True

    for u in settings.users:
        if u['username'] == user.username:
            access = True

            if u['period']:
                period_end = datetime.strptime(u['period'], '%d.%m.%Y')
                cur_time = datetime.now()

                if cur_time > period_end:
                    access = False

    if not access:
        await event.respond('Нет доступа, обратитесь к администратору')

    return access
