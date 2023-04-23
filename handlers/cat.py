from aiogram import types

from loader import dp, cat_api


@dp.message_handler(commands=['cat'])
async def get_random_cat_image(message: types.Message):
    """
    Отправка рандомной картинки с котиком
    @param message: telegram message
    @return:
    """
    photo_url = await cat_api.get_cat_url()
    await message.answer_photo(photo_url)
