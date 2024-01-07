import logging
from aiogram import Bot, Dispatcher, types
from gpt import ask_gpt
from weather import weather_command
import os

#os.environ['OPENAI_API_KEY'] = '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'

#TELEGRAM_TOKEN = '6796223846:AAEfMMtEuM11tAa4kGV0KvrsOShUD_OxLP8'
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)  # Передаем экземпляр Bot в Dispatcher

# Настройка логирования
logging.basicConfig(filename='bot_log.txt', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logger.info("Обработка команды start")
    response = ("Привет! Я асинхронный бот, использующий AI для ответов.\n"
                "Служебные команды:\n"
                "/weather - погода на день, неделю;\n"
                "Для общения со мной просто напишите сообщение.")
    await message.reply(response)

# Обработчик команды /weather
@dp.message_handler(commands=['weather'])
async def handle_weather_command(message: types.Message):
    command_args = message.get_args().split()  # Получаем аргументы команды
    await weather_command(message, command_args)

# Обработчик упоминаний бота
@dp.message_handler(lambda message: '@b643_bot' in message.text)
async def handle_mention(message: types.Message):
    question = message.text.replace('@b643_bot', '').strip()
    answer = await ask_gpt(question)
    await message.reply(answer)

# Обработчик текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type == "private":
        question = message.text
        if not question.strip():
            await message.reply("Пожалуйста, введите вопрос.")
            return
        answer = await ask_gpt(question)
        await message.reply(answer)

# Асинхронная функция запуска бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
