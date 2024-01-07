import requests
import asyncio
from datetime import datetime
from aiogram import types

api_key = "5303a10dda03b3d565216a831e161165"

async def get_weather(city, period='daily'):
    if period == 'daily':
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            # Тело функции остаётся таким же
            ...
        else:
            return "Произошла ошибка при получении данных о погоде."
    except Exception as e:
        return f"Произошла ошибка при обработке запроса к API погоды: {e}"

async def weather_command(message: types.Message, args):
    if len(args) >= 1:
        city = args[0]
        period = 'weekly' if len(args) > 1 and args[1].lower() == 'week' else 'daily'
        weather_info = await get_weather(city, period)
        await message.reply(weather_info)
    else:
        await message.reply("Для получения погоды используйте команды...")
