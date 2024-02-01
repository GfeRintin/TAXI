from aiogram import types, Dispatcher
from creat_bot import dp, bot, db, TOKEN


async def check_reg(message: types.Message):
    if not bool(len(db.subscriber_exists(message.from_user.id))):
        await bot.send_message(message.chat.id, text="Извините, чтобы пользоваться ботом, нужно пройти регистрацию:\n/start")
        return False
    elif db.subscriber_exists(message.from_user.id)[0][8] == None:
        await bot.send_message(message.chat.id, text="Извините, чтобы пользоваться ботом, нужно добавить свой номер телефона:\n/start")
        return False
    else:
        return True