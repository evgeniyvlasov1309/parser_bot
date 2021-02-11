from telethon import Button

from data import config
from loader import client

CATEGORIES = ['смм', 'дизайн', 'wordpress', 'маркетинг']

category_keyboard = []
sub_array = []

for category in CATEGORIES:
    sub_array.append(Button.inline(category))

    if len(sub_array) == 2:
        category_keyboard.append(sub_array)
        sub_array = []
