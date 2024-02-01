import os
import logging
import TOKEN
# import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB.SQLDateBase import SQLighter

from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN.Token)
dp = Dispatcher(bot, storage=MemoryStorage())
#dp.message_handlers.once = False 

# инициализируем соединение с БД
db = SQLighter(TOKEN.DB)

# #логирование
# logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')
# warning_log = logging.getLogger("warning_log")
# warning_log.setLevel(logging.WARNING)

# fh = logging.FileHandler("warning_log.log")

# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)

# warning_log.addHandler(fh)