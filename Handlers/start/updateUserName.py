from creat_bot import db
from aiogram import types

# update user_name
def updateUserName(message: types.Message):
    if bool(message.chat.username):
        if message.chat.username == db.subscriber_exists(message.chat.id)[0][2]:
            pass
        else:
            db.update_UserName(message.chat.id, message.chat.username)
    else:
        pass
