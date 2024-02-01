import os
import logging
import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB.SQLDateBase import SQLighter

from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN.Token)
dp = Dispatcher(bot, storage=MemoryStorage())
#dp.message_handlers.once = False 

# инициализируем соединение с БД
db = SQLighter(TOKEN.DB)

