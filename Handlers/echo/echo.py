from aiogram import types, Dispatcher 
from creat_bot import bot
from creat_bot import TOKEN 
from TOKEN import chatId


# echo bot
#@dp.message_handler(content_types=["text", "photo"])
async def handle_text(message: types.Message):
    markup = types.InlineKeyboardMarkup()    
    markup.add(types.InlineKeyboardButton(text='↪️ Вернуться в меню',  callback_data = "menu"))
    if message.chat.id == TOKEN.chatId:
        pass
    elif message.chat.id == -703016769:
        pass
    elif bool(message.text):
        await bot.send_message(message.chat.id, 'Вы написали: ' + message.text + '. Я не знаю что мне с этим делать\n'"", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, 'Вы прислали: ')
        await bot.forward_message(message.chat.id, message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, ' Я не знаю что мне с этим делать', reply_markup=markup)

def register_handler_echo_bot(dp: Dispatcher):
    dp.register_message_handler(handle_text, content_types=["text", "photo"])