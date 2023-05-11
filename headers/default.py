from aiogram import Router, types
from kb.kb import *
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

router = Router()

q = ''
numbers = []
number = 0
attempts_left = 0
secret_number = 0


class Answer_Handler(StatesGroup):
    answer = State()
    say = State()


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    await message.answer('Привет, чтобы начать игру "Угадай число", нажми кнопку ниже', reply_markup=start_kb())
    await message.delete()


@router.callback_query(lambda c: c.data == 'start')
async def stater_pack(call: types.CallbackQuery):
    await call.message.answer('Выбери кто загадывает!', reply_markup=game_kb())
    await call.message.delete()


@router.callback_query(lambda c: c.data == 'you')
async def yourself(call: types.CallbackQuery, state: FSMContext):
    global q, numbers, number
    numbers = [3, 4, 5, 6, 7]
    more_less = ['больше', 'меньше']
    number = random.randint(3, 8)
    q = random.choice(more_less)
    await call.message.answer(f'Ваше число {q} {number} ?\nПиши ответ в виде сообщения')
    await state.set_state(Answer_Handler.answer)
    await call.message.delete()


@router.callback_query(lambda c: c.data == 'bot_work')
async def bot_self(call: types.CallbackQuery, state: FSMContext):
    global secret_number, attempts_left
    secret_number = random.randint(1, 10)
    attempts_left = 5
    await call.message.answer(f'Я загадал число от 1 до 10, попробуй отгадать!\nУ тебя есть 5 попыток!\nНапиши число:')
    await state.set_state(Answer_Handler.say)
    await call.message.delete()


@router.message(Answer_Handler.say)
async def user_play(message: types.Message, state: FSMContext):
    global secret_number, attempts_left
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
    guess = int(message.text)
    attempts_left -= 1
    if guess == secret_number:
        await message.answer(f"Поздравляю, ты угадал число!"
                             f" Это было число {secret_number}.\nЕсли хочешь сыграть ещё нажми 'Старт'",
                             reply_markup=start_kb())
        await state.clear()
    elif guess > secret_number:
        await message.answer(f"Твое число слишком большое. Осталось попыток: {attempts_left}.")
    else:
        await message.answer(f"Твое число слишком маленькое. Осталось попыток: {attempts_left}.")
    if attempts_left == 0:
        await message.answer(f"К сожалению, ты не угадал число."
                             f" Это было число {secret_number}.\nЕсли хочешь сыграть ещё нажми 'Старт'",
                             reply_markup=start_kb())
        await state.clear()


@router.message(Answer_Handler.answer)
async def user_play(message: types.Message, state: FSMContext):
    global number, q
    default = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    new_numbers = []
    await state.update_data(answer=message.text)
    data = await state.get_data()
    try:
        if ('да' in data['answer']) or ('Да' in data['answer']):
            if q == 'больше':
                for i in range(len(default)):
                    if default[i] > number:
                        new_numbers.append(default[i])
            if q == 'меньше':
                for i in range(len(default)):
                    if default[i] < number:
                        new_numbers.append(default[i])
        if ('нет' in data['answer']) or ('Нет' in data['answer']):
            if q == 'больше':
                for i in range(len(default)):
                    if default[i] < number:
                        new_numbers.append(default[i])
            if q == 'меньше':
                for i in range(len(default)):
                    if default[i] > number:
                        new_numbers.append(default[i])
        await message.answer(f'Ваше число {random.choice(new_numbers)} ?',
                             reply_markup=gameover_kb())
    except Exception as err:
        print(err)
    await state.clear()
    await message.delete()


@router.callback_query(lambda c: c.data == 'win')
async def winner(call: types.CallbackQuery):
    await call.message.answer('Я выиграл!\nЕсли хочешь сыграть еще раз, жми кнопку ниже.',
                         reply_markup=start_kb())
    await call.message.delete()


@router.callback_query(lambda c: c.data == 'lose')
async def loser(call: types.CallbackQuery):
    await call.message.answer('Я проиграл :(!\nЕсли хочешь сыграть еще раз, жми кнопку ниже.',
                         reply_markup=start_kb())
    await call.message.delete()
