from aiogram import types, Dispatcher 
from creat_bot import dp, bot, db, TOKEN
from TOKEN import AdminID

async def CheckAdmin(message):
    test = int(message)
    for data in db.all_admin():
        if data[0] == test:
            return True
    return False
    
