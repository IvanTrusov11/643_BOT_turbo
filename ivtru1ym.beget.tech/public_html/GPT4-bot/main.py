from aiogram import Bot, Dispatcher, executor, types
from config.config import TELEGRAM_TOKEN
import bot_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Измените эту строку
bot_handlers.register_handlers(dp, bot)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)