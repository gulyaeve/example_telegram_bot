from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.keyboards import location_button
from loader import dp, messages, weather_api


class WeatherStates(StatesGroup):
    Location = State()


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['weather'])
async def weather_start(message: types.Message):
    await message.answer(await messages.get_message("weather_get_location"), reply_markup=location_button)
    await WeatherStates.Location.set()


@dp.message_handler(state=WeatherStates.Location, content_types=types.ContentType.LOCATION)
async def weather_location(message: types.Message, state: FSMContext):
    weather = await weather_api.get_weather(message.location.latitude, message.location.longitude)
    await message.reply(str(weather), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=WeatherStates.Location, content_types=types.ContentType.ANY)
async def weather_no_location(message: types.Message):
    return await message.reply(await messages.get_message("weather_no_location"))

