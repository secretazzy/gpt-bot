import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from openai import AsyncOpenAI

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
AGENTROUTER_API_KEY = os.getenv("AGENTROUTER_API_KEY")

client = AsyncOpenAI(
    api_key=AGENTROUTER_API_KEY,
    base_url="https://agentrouter.org/v1"
)

dp = Dispatcher()
bot = Bot(token=TG_BOT_TOKEN)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Бот готов к работе!")

@dp.message(F.text)
async def text_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        res = await client.chat.completions.create(
            model="gpt-6-astra",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(res.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
