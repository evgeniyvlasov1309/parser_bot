from telethon import Button


def get_categories_keyboard(categories):
    category_keyboard = []
    sub_array = []

    for (index, category) in enumerate(categories):
        sub_array.append(Button.inline(category['label'], data=f'category {index}'))

        if len(sub_array) == 3:
            category_keyboard.append(sub_array)
            sub_array = []
        elif index == len(categories) - 1:
            category_keyboard.append(sub_array)

    return category_keyboard
