from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

API_ID = env.str("API_ID")
API_HASH = env.str("API_HASH")
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
CHANNELS = env.list("CHANNELS")
