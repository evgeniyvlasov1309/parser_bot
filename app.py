from telethon import events, Button

from data import config
from keyboards.inline import category_keyboard
from loader import client, bot
from utils.functions import get_messages_from_channels


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await bot.send_message(event.peer_id,
                           'Добро пожаловать!\n\nВведите ключевое слово для поиска вакансий, либо укажите категорию:',
                           buttons=category_keyboard)
    raise events.StopPropagation


@bot.on(events.CallbackQuery())
async def button_request(event):
    text = event.data.decode('utf8')
    await event.respond(f'Получено сообщение: {text}')
    # messages = await get_messages_from_channels(config.CHANNELS, text)
    # messages_total = len(messages)
    # if messages_total:
    #     await event.respond(f'Найдено: {messages_total}')
    #     for message in messages:
    #         bot.send_message(event.peer_id, message)
    # else:
    #     await event.respond('К сожалению, по заданному ключевому слову ничего не найдено')
    await event.answer()


@bot.on(events.NewMessage())
async def echo(event):
    print(event.peer_id)
    await event.respond(f'Получено сообщение: {event.text}')
    # messages = await get_messages_from_channels(config.CHANNELS, event.text)
    # messages_total = len(messages)
    # if messages_total:
    #     await event.respond(f'Найдено: {messages_total}')
    #     for message in messages:
    #         bot.send_message(event.peer_id, message)
    # else:
    #     await event.respond('К сожалению, по заданному ключевому слову ничего не найдено')

    # async def main():
    #     print('hey')
    #     client_info = await client.get_me()
    #     bot_info = await bot.get_me()
    #     await client.send_message('+79199520444', 'Привет сучара')
    #     await bot.forward_messages(602781007, message)
    #     async for message in client.iter_messages('+79199520444'):
    #         print(message.stringify())
    #         # await client.delete_messages(, message)
    #         if message.message:
    #             await bot.forward_messages(602781007, message)

    if __name__ == '__main__':
        print('hey')
        client.run_until_disconnected()
