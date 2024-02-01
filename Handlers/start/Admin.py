from creat_bot import db


async def CheckAdmin(message):
    test = int(message)
    for data in db.all_admin():
        if data[0] == test:
            return True
    return False
    
