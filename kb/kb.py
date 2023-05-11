from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Старт', callback_data='start'),
    return keyboard.as_markup(resize_keyboard=True)


def gameover_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Да', callback_data='win'),
    keyboard.button(text='Нет', callback_data='lose'),
    return keyboard.as_markup(resize_keyboard=True)


def game_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Я загадывю!', callback_data='you'),
    keyboard.button(text='Бот загадывает!', callback_data='bot_work'),
    return keyboard.as_markup(resize_keyboard=True)
