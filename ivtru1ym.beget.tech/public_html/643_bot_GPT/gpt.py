import openai
import asyncio
import os

# Устанавливаем API ключ OpenAI
api_key = os.environ.get('OPENAI_API_KEY', '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')

async def ask_gpt(question):
    try:
        # Используем asyncio для асинхронного выполнения синхронного вызова
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка при запросе к OpenAI: {e}"
