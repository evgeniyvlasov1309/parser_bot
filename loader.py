from telethon import TelegramClient

from data import config

client = TelegramClient('user', config.API_ID, config.API_HASH)
client.start()

bot = TelegramClient('bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)