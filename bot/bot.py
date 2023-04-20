import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config.config import TOKEN

start_message = "Привет! Я загадал число от 1 до 10. Попробуй угадать за 5 попыток.\nВведи число:"


def bot():
    bot_initial = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot_initial, storage=storage)

    class GuessNumber(StatesGroup):
        guess = State()

    @dp.message_handler(commands=['start', 'reset'])
    async def start(message: types.Message, state: FSMContext):
        answer = random.randint(1, 10)
        await message.answer(start_message)
        await GuessNumber.guess.set()
        await state.update_data(answer=answer)

    @dp.message_handler(state=GuessNumber.guess)
    async def guess_number(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            user_number = int(message.text)
            data_number = await state.get_data()
            answer = data_number.get("answer")
            if user_number == answer:
                await message.answer("Поздравляю, ты угадал число!")
                await state.finish()
            else:
                await message.answer("Неправильно. Попробуй еще раз.")

            data_attempts = await state.get_data()
            attempts = data_attempts.get("attempts")
            if attempts is None:
                attempts = 0
            attempts += 1
            if attempts == 5:
                await message.answer(f"Ты использовал все 5 попыток. Я загадал число {answer}. Попробуй снова!")
                await state.finish()
            else:
                await state.update_data(attempts=attempts)
        else:
            await message.answer("Неправильный формат числа. Введи число от 1 до 10.")

    executor.start_polling(dp, skip_updates=True)
