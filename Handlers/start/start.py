import asyncio
from aiogram import types, Dispatcher
from creat_bot import bot, db, TOKEN, SQLighter
from Handlers.menu import menu as mn
import traceback
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#класс машины состояний
class cabinet_check(StatesGroup):
    msg1 = State()
    msg2 = State()


# start
# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Регистрируем пользователя
    print("TAXI_bot")
    try:
        if not bool(len(db.subscriber_exists(message.chat.id))):
            await _start_(message)          
        else:
            await bot.send_message(message.chat.id, text ="""🚕 Добро пожаловать в наш телеграмм-бот для вызова такси! \nЗдесь вы можете быстро и удобно заказать машину. \nОзнакомьтесь с нашими услугами и наслаждайтесь комфортной поездкой! 🌟🚖""", reply_markup=types.ReplyKeyboardRemove() )
            await mn.menu(message)
    except Exception as e:
        traceback.print_exc()
        print(e)


# Добавляем пользователя в базу
async def _start_(message: types.Message):

    # если юзера нет в базе, добавляем его
    if not bool(len(db.subscriber_exists(message.from_user.id))):
        if bool(message.from_user.username):
            db.add_subscriber(message.from_user.id, username=message.from_user.username,
                              first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        else:
            db.add_subscriber(message.from_user.id, username=0,
                              first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        await bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + '👋')
        await bot.send_message(message.chat.id, text ="""🚕 Добро пожаловать в наш телеграмм-бот для вызова такси!\nЗдесь вы можете быстро и удобно заказать машину. \nОзнакомьтесь с нашими услугами и наслаждайтесь комфортной поездкой! 🌟🚖""" )
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = [
            types.KeyboardButton(text='☎️ - Отправить номер телефона', request_contact=True, one_time_keyboard =True),
            ]
        markup.add(*button)
        await bot.send_message(message.chat.id, text ="🔶 Прежде чем начать пользоваться нашим ботом, убедитесь, что у вас указан ваш номер телефона. Это необходимо для регистрации и дальнейшего заказа такси. ☎️🚖", reply_markup=markup)

async def add_phone(message: types.Message):
    contact = message.contact
    await bot.send_message(message.chat.id, text=f"Спасибо, {contact.full_name}.\n"+
                         f"Ваш номер {contact.phone_number} был получен",
                         reply_markup=types.ReplyKeyboardRemove())
    db.add_phone(contact.phone_number, message.from_user.id)
    await mn.menu(message)
    await newUsers(message)                

# сообщение о новом пользователе
async def newUsers(message: types.Message):
    new_user = types.InlineKeyboardMarkup()
    if bool(message.from_user.username):
        info_user = types.InlineKeyboardButton(text=str(message.from_user.first_name), url=str('https://t.me/' + message.from_user.username))
        new_user.add(info_user)
        await bot.send_message(TOKEN.adminChatId, "У вас новый пользователь:", reply_markup=new_user)
    else:
        await bot.send_message(TOKEN.adminChatId, "У вас новый пользователь:\n" + str(message.from_user.first_name))



def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(add_phone, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(start, commands=['start'])
