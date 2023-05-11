from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import Token
from headers import default
import asyncio


async def start_bot():
    bot = Bot(Token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(default.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())

