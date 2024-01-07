from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import openai
import aiohttp
import asyncio
from io import BytesIO
import subprocess
import logging
import json
from aiohttp import FormData
from config.config import OPENAI_API_KEY, TELEGRAM_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Словарь для хранения истории чатов
chat_histories = {}

class ChatState(StatesGroup):
    waiting_for_message = State()

async def start_command(message: types.Message, bot):
    await message.answer("Привет! Я асинхронный бот, использующий AI для ответов.")
    await ChatState.waiting_for_message.set()

async def chat(message: types.Message, state: FSMContext, bot):
    chat_id = message.chat.id
    if message.chat.type != 'private' and '@b643_bot' not in message.text:
        return

    question = message.text.replace('@b643_bot', '').strip() if message.chat.type in ["group", "supergroup"] else message.text

    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    chat_histories[chat_id].append({"role": "user", "content": question})

    if len(chat_histories[chat_id]) > 10:
        chat_histories[chat_id] = chat_histories[chat_id][-10:]

    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
    data = {
        'model': "gpt-4-1106-preview",
        'messages': chat_histories[chat_id]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        answer = response_data['choices'][0]['message']['content']
        await message.answer(answer)
        chat_histories[chat_id].append({"role": "assistant", "content": answer})
    else:
        await message.answer("Произошла ошибка при обработке вашего запроса.")

    await ChatState.waiting_for_message.set()

async def cancel_command(message: types.Message, state: FSMContext, bot):
    await state.finish()
    await message.answer("Диалог завершен.")

async def convert_ogg_to_mp3(ogg_data):
    src = BytesIO(ogg_data)
    dest = BytesIO()
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', 'pipe:0', '-f', 'mp3', 'pipe:1',
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate(input=src.read())
    if process.returncode != 0:
        logging.error(f"Ошибка конвертации: {stderr.decode()}")
        return None
    dest.write(stdout)
    dest.seek(0)
    return dest

async def handle_voice_message(message: types.Message, bot: Bot):
    logging.info("Обработка голосового сообщения")
    try:
        file_id = message.voice.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status != 200:
                    logging.error(f"Ошибка загрузки файла: {resp.status}")
                    return
                ogg_data = await resp.read()

        data = FormData()
        data.add_field('file', ogg_data, filename='audio.ogg', content_type='audio/ogg')
        data.add_field('model', 'whisper-1')

        headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, data=data) as resp:
                response_data = await resp.json()
                if resp.status != 200:
                    logging.error(f"Ошибка запроса в OpenAI: {resp.status}, ответ: {response_data}")
                    return
                logging.info(f"Ответ OpenAI: {response_data}")
                transcript = response_data.get('text', 'Не удалось получить транскрипцию')
                logging.info(f"Транскрипция получена: {transcript}")
                await message.reply(transcript)

    except Exception as e:
        logging.error(f"Ошибка обработки голосового сообщения: {e}")
        await message.reply(f"Произошла ошибка: {e}")

def register_handlers(dp: Dispatcher, bot):
    dp.register_message_handler(lambda msg: start_command(msg, bot), commands=["start"], state="*")
    dp.register_message_handler(lambda msg, state: chat(msg, state, bot), state=ChatState.waiting_for_message)
    dp.register_message_handler(lambda msg, state: cancel_command(msg, state, bot), commands=["cancel"], state="*")
    dp.register_message_handler(lambda msg: handle_voice_message(msg, bot), content_types=['voice'])
