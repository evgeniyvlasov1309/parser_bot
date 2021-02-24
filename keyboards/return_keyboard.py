from telethon import Button

from classes.Settings import settings


def get_return_keyboard(length):
    if length > settings.pagination:
        return [Button.text(text='Показать еще', resize=True, single_use=True),
                Button.text(text='Вернуться в начало', resize=True, single_use=True)]
    else:
        return [Button.text(text='Вернуться в начало', resize=True, single_use=True)]
