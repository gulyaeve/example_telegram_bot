from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

poll_finish = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Завершить создание опроса",
                callback_data="finish_poll"
            )
        ]
    ]
)


select_group = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Выбрать",
                callback_data="pollgroup_0"
            )
        ]
    ]
)
