from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from db import *

from services import *
import keyboards as kb

API_TOKEN = '5567026628:AAG4DT_i8npBy94m6LLlFkrp_B9s1tos2ns'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Cities(StatesGroup):
    city_name = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    initizlize()
    await Cities.city_name.set()
    await bot.send_message(message.from_user.id, f"Привет {message.from_user.full_name}, введи название города или его части")


@dp.message_handler(state=Cities.city_name)
async def share_reviews_first(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city_name'] = message.text
    await state.finish()
    if cities := find_cities(data['city_name']):
        await bot.send_message(message.from_user.id, 'Выберите город из списка', reply_markup=kb.keyboard_1(cities))
    else:
        await bot.send_message(message.from_user.id, f'Увы, не получилось ничего найти по запросу {data["city_name"]}\n\nЧтобы попробовать заново нажмите\n/start')

@dp.callback_query_handler(kb.callback_numbers.filter())
async def callback_data(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    city = get_city(int(action))
    await call.message.edit_text(f"<b>Город:</b> <a href=\'https://ru.wikipedia.org{city[2]}\'>{city[1]}</a>\n<b>Городской округ:</b> <a href=\'https://ru.wikipedia.org{city[4]}\'>{city[3]}</a>\n<b>Население:</b> {city[5]}", parse_mode='HTML')

    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
