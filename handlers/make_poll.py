import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_inline_paginations.paginator import Paginator

from keyboards.poll_keyboards import poll_finish, select_group
from loader import dp, messages, groups


class PollStates(StatesGroup):
    InputOption = State()
    Confirm = State()


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['make_poll'])
async def make_poll(message: types.Message):
    await message.answer(await messages.get_message("poll_start_make"))
    await PollStates.InputOption.set()


@dp.message_handler(state=PollStates.InputOption, content_types=types.ContentType.TEXT)
async def input_option(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'poll' in data.keys():
            data['poll'].append(message.text)
        else:
            data['poll'] = [message.text]
    if len(data['poll']) >= 3:
        await message.reply(await messages.get_message("poll_input_option"), reply_markup=poll_finish)
    else:
        await message.reply(await messages.get_message("poll_input_option"))


@dp.callback_query_handler(state=PollStates.InputOption, text='finish_poll')
async def make_poll_finish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(await messages.get_message("poll_make_finish"), reply_markup=select_group)
    await PollStates.Confirm.set()


@dp.message_handler(state=PollStates.InputOption, content_types=types.ContentType.ANY)
async def input_option(message: types.Message):
    return await message.reply(await messages.get_message("poll_input_text"))


@dp.callback_query_handler(Text(startswith='pollgroup_'), state=PollStates.Confirm)
# @dp.callback_query_handler(text=AdminCallbacks.get_users.value)
async def get_users(callback: types.CallbackQuery):
    await callback.answer("Выгружаю")
    page_n = 0
    if callback.data.startswith("pollgroup_"):
        page_n = int(callback.data.split("_")[1])
    groups_list = await groups.select_all_groups()
    if not groups_list:
        return await callback.message.answer(await messages.get_message("poll_not_groups"))
    buttons_users = types.InlineKeyboardMarkup()
    for group in groups_list:
        buttons_users.add(group.make_button())
    logging.info(buttons_users)
    users_inline = Paginator(callback_startswith="pollgroup_", data=buttons_users)
    await callback.message.edit_text("Готово:", reply_markup=users_inline(current_page=page_n))


@dp.callback_query_handler(Text(startswith="pollgroup="), state=PollStates.Confirm)
async def send_poll_to_group(callback: types.CallbackQuery, state: FSMContext):
    group_id = callback.data.split("=")[1]
    poll = (await state.get_data())['poll']
    await dp.bot.send_poll(
        chat_id=group_id,
        question=poll[0],
        options=poll[1:],
    )
    await callback.answer("Опрос отправлен!", show_alert=True)
    logging.info(f"{callback.from_user.id} отправил опрос {poll} в группу {group_id}")
    await state.finish()
