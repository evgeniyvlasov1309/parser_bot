from telethon import Button


def get_time_keyboard(times):
    time_keyboard = []
    sub_array = []

    for (index, time) in enumerate(times):
        sub_array.append(Button.inline(time['label'], data=f'time {index}'))

        if len(sub_array) == 2:
            time_keyboard.append(sub_array)
            sub_array = []
        elif index == len(times) - 1:
            time_keyboard.append(sub_array)

    return time_keyboard
