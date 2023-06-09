import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import Config
from utils.cat_api import CatApi
from utils.db_api.db import Database
from utils.db_api.groupsdb import GroupsDB
from utils.db_api.usersdb import UsersDB
from utils.db_api.messages import Messages
from utils.admin_page_rest_api import AdminPageRestAPI
from utils.exchange_rates_api import ExchangeRatesApi
from utils.weather_api import OpenWeatherApi

# ChatBot objects
if Config.proxy_url:
    bot = Bot(
        token=Config.telegram_token,
        parse_mode=types.ParseMode.HTML,
        proxy=Config.proxy_url,
    )
else:
    bot = Bot(
        token=Config.telegram_token,
        parse_mode=types.ParseMode.HTML,
    )
storage = RedisStorage2(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
)
dp = Dispatcher(
    bot=bot,
    storage=storage,
)

# Users from database
users = UsersDB()
# Groups from database
groups = GroupsDB()
# Messages from database
messages = Messages()

# REST_API for admin application
loop = asyncio.get_event_loop()
bot_info: types.User = loop.run_until_complete(dp.bot.get_me())
if Config.rest_link:
    admin_api = AdminPageRestAPI(bot_info.to_python())
else:
    admin_api = None

# OpenWeatherApi
weather_api = OpenWeatherApi()

# ExchangeRatesAPI
exchange_api = ExchangeRatesApi()

# CatAPI
cat_api = CatApi()

# Logging setup
logging.basicConfig(
    handlers=(logging.FileHandler('logs/log.txt'), logging.StreamHandler()),
    format=u'%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s',
    level=logging.INFO,
)
