from creat_bot import types, Dispatcher
from creat_bot import bot

async def new_user(message: types.Message):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    
    invited_user = message.new_chat_members[0]        # Кого пригласили в группу
    who_invited = message.from_user                  # Кто пригласил
    

def register_handler(dp: Dispatcher):
    dp.register_message_handler(new_user, content_types=['new_chat_members'])