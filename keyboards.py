from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

callback_numbers = CallbackData("fabnum", "action")


def keyboard_1(cities: list):
    buttons = [InlineKeyboardButton(text=f"{city[1]} ({city[3]})", callback_data=callback_numbers.new(action=int(city[0]))) for city in cities]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
