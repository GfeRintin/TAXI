from aiogram import types
from creat_bot import dp, bot, db


async def check_reg(message: types.Message):
    if not bool(len(db.subscriber_exists(message.from_user.id))):
        await bot.send_message(message.chat.id, text="Простите, но для того, чтобы воспользоваться нашим ботом, требуется прохождение регистрации↩️\n/start")
        return False
    elif db.subscriber_exists(message.from_user.id)[0][8] == None:
        await bot.send_message(message.chat.id, text="Простите, но для того, чтобы воспользоваться нашим ботом, требуется добавить свой номер телефона↩️\n/start")
        return False
    else:
        return True