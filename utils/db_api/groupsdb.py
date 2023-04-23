from dataclasses import dataclass
from typing import Sequence

import asyncpg
import asyncio

from aiogram.types import InlineKeyboardButton

from utils.db_api.db import Database


@dataclass
class Group:
    telegram_id: int
    full_name: str

    def make_button(self):
        return InlineKeyboardButton(
            text=f"{self.full_name}",
            callback_data=f"pollgroup={self.telegram_id}",
        )


class Groups:
    def __init__(self, users: Sequence[Group]):
        self._users = users

    def __getitem__(self, key: int) -> Group:
        return self._users[key]


class GroupsDB(Database):
    def __init__(self):
        super().__init__()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tables())

    async def create_tables(self):
        sql = """CREATE TABLE IF NOT EXISTS groups (
            telegram_id bigint NOT NULL UNIQUE PRIMARY KEY,
            full_name character varying(255) NOT NULL
        );
        """
        await self._execute(sql, execute=True)

    # Пользователи
    async def _format_group(self, record: asyncpg.Record) -> Group:
        return Group(
            telegram_id=record['telegram_id'],
            full_name=record['full_name'],
        )

    async def add_group(self, telegram_id: int, full_name: str) -> Group:
        """
        Добавление группы в базу данных

        :param full_name: group's fullname from telegram
        :return:
        """
        sql = "INSERT INTO groups (telegram_id, full_name) VALUES($1, $2) returning *"
        record = await self._execute(sql, telegram_id, full_name, fetchrow=True)
        return await self._format_group(record)

    async def update_group_fullname(self, full_name: str, telegram_id: int):
        sql = "UPDATE groups SET full_name=$1 WHERE telegram_id=$2"
        return await self._execute(sql, full_name, telegram_id, execute=True)

    async def select_all_groups(self) -> Groups:
        sql = "SELECT * FROM groups"
        list_of_records = await self._execute(sql, fetch=True)
        return Groups([await self._format_group(record) for record in list_of_records])

    # async def select_user(self, **kwargs) -> asyncpg.Record:
    #     sql = "SELECT * FROM users WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetchrow=True)

    async def select_group(self, telegram_id: int) -> Group:
        sql = "SELECT * FROM groups WHERE telegram_id=$1"
        record = await self._execute(sql, telegram_id, fetchrow=True)
        return await self._format_group(record)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM groups"
        return await self._execute(sql, fetchval=True)

    # async def delete_user(self, telegram_id):
    #     await self._execute("DELETE FROM users WHERE telegram_id=$1", telegram_id, execute=True)
    #
    # async def delete_users(self):
    #     await self._execute("DELETE FROM users WHERE TRUE", execute=True)
    #
    # async def drop_users(self):
    #     await self._execute("DROP TABLE IF EXISTS users CASCADE ", execute=True)
