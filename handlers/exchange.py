from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, messages, exchange_api
from utils.utilities import make_keyboard_list


class ExchangeStates(StatesGroup):
    To = State()
    Amount = State()
    Result = State()


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['exchange'])
async def start_exchange(message: types.Message):
    currency_list = ['USD', 'EUR', 'RUB']
    await message.answer(
        text=await messages.get_message("exchange_select_from"),
        reply_markup=make_keyboard_list(currency_list),
    )
    await ExchangeStates.To.set()


@dp.message_handler(state=ExchangeStates.To)
async def exchange_to(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['from'] = message.text
    currency_list = ['USD', 'EUR', 'RUB']
    await message.answer(
        text=await messages.get_message("exchange_select_to"),
        reply_markup=make_keyboard_list(currency_list),
    )
    await ExchangeStates.Amount.set()


@dp.message_handler(state=ExchangeStates.Amount)
async def exchange_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['to'] = message.text
    await message.answer(
        text=await messages.get_message("exchange_input_amount"),
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ExchangeStates.Result.set()


@dp.message_handler(state=ExchangeStates.Result)
async def exchange_get_result(message: types.Message, state: FSMContext):
    if int(message.text):
        amount = int(message.text)
        data = await state.get_data()
        exchange_result = await exchange_api.get_exchange(
            exchange_from=data['from'],
            exchange_to=data['to'],
            amount=amount
        )
        if exchange_result:
            await message.reply(
                text=f"Результат конвертации {amount} из {data['from']} в {data['to']}: <b>{exchange_result}</b>",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.reply(
                text=await messages.get_message("api_error"),
                reply_markup=types.ReplyKeyboardRemove()
            )
        await state.finish()
    else:
        return await messages.get_message("exchange_input_digit")