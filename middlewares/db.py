from logging import log, INFO

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.admins.admins import notify_admins
from loader import users, groups


class DBmiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        try:
            user = await users.select_user(message.from_user.id)
            if user is not None:
                if user.full_name != message.from_user.full_name:
                    await users.update_group_fullname(message.from_user.full_name, message.from_user.id)
                    log(INFO, f"Updated full_name [{message.from_user.full_name}] for [{message.from_user.id}]")
                if user.username != message.from_user.username:
                    await users.update_user_username(message.from_user.username, message.from_user.id)
                    log(INFO, f"Updated username [{message.from_user.username}] for [{message.from_user.id}]")
        except:
            new_user = await users.add_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
            await notify_admins(f"<b>Добавлен пользователь:</b>\n{new_user.get_info()}")
            log(INFO, f"Added user to db [{new_user}]")

    async def on_process_message(self, message: types.Message, data: dict):
        chat_type = message.chat.type
        if chat_type == types.ChatType.GROUP or chat_type == types.ChatType.SUPERGROUP:
            log(INFO, f"{chat_type=} {message.chat.id=} {message.chat.full_name=}")
            group = await groups.select_group(message.chat.id)
            if not group:
                new_group = await groups.add_group(message.chat.id, message.chat.full_name)
                log(INFO, f"Added group to db [{new_group}]")
            if group.full_name != message.chat.full_name:
                await groups.update_group_fullname(message.chat.full_name, message.chat.id)
                log(INFO, f"Updated full_name [{message.chat.full_name}] for [{message.chat.id}]")
