from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from creat_bot import dp, bot, db, TOKEN
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import json

from Handlers.start import updateUserName as uun

import requests
import asyncio
import datetime
from Handlers.echo.check_reg import check_reg 

class From(StatesGroup):
    comment = State()
   

location_data = CallbackData("none", "action", "func", "mes_id")
order_id_data = CallbackData("none", "id_db", "func", "user_id")
comment_data = CallbackData("none", "action", "func", "id_db")

def get_address_from_coords(coords):
    """Запрос в яндекс, который получает адрес"""
    #заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
    PARAMS = {
        "apikey":"bd9f2337-293e-49f9-98a7-75b305e04b41",
        "format":"json",
        "lang":"ru_RU",
        "kind":"house",
        "geocode": coords
    }

    #отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        #возвращаем полученный адрес
        return address_str
    except Exception as e:
        #если не смогли, то возвращаем ошибку
        print(e)
        return "error"

async def location(message: types.Message):
    if not check_reg:
        return
    uun.updateUserName(message)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    button = [
        types.KeyboardButton(text='🆘 - Отправить заявку, нажимай сюда.', request_location = True, callback_data="geo", one_time_keyboard =True),
        ]
    markup.add(*button)
    await bot.send_message(message.chat.id, text = 'Чтобы вызвать такси, отправьте свою геолокацию', reply_markup = markup)

async def get_location(message: types.Message):
    if not check_reg:
        return
    
    if db.order_finish__exists_client(message.chat.id) != None:
        await bot.send_message(message.chat.id, text ="У вас уже есть не завершённый заказ, если есть проблемы сообщите в поддержку\n /help - поддержка")
        return

    uun.updateUserName(message)
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(coords)
    #address_str = "Россия, Санкт-Петербург, проспект Культуры, 6к3 тест"
    #вовщращаем результат пользователю в боте
    markup = types.ReplyKeyboardRemove()
    mes = await bot.send_message(message.chat.id, text ="Обрабатываем...⏳", reply_markup=markup)
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
    markup = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text='✅', callback_data=location_data.new(action=True, func="location", mes_id=message.message_id)),
        types.InlineKeyboardButton(text='❌', callback_data=location_data.new(action=False, func="location", mes_id=message.message_id)),
        ]
    markup.add(*button)
    await bot.send_message(message.chat.id, text =address_str, reply_markup=markup)


async def new_order(call: CallbackData, callback_data:dict):
    """Принимаем новый заказ"""
    if callback_data.get("action") == "False":
        # Если не согласен с адресом или передумал
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = [
            types.KeyboardButton(text='🆘 - Отправить заявку, нажимай сюда.', request_location = True, callback_data="geo", one_time_keyboard =True),
            ]
        markup.add(*button)
        await call.message.edit_text(text ="Заказ отменён!")
        return
    elif callback_data.get("action") == "True":
        await call.message.edit_text(text=call.message.text)
        await bot.forward_message(chat_id=TOKEN.chatId, from_chat_id=call.message.chat.id, message_id=callback_data.get('mes_id'))

        #Создаем заказ в БД
        db.new_order(address=call.message.text, create_order=datetime.datetime.now().strftime("%d/%m/%y %H:%M"), phone=db.subscriber_exists(call.message.chat.id)[0][8], user_id=call.message.chat.id)

        markup = types.InlineKeyboardMarkup(row_width=1)
        button = [
            types.InlineKeyboardButton(text='Беру заказ себе↩️', callback_data=order_id_data.new(id_db=str(db.get_order_last()[0][0]), func='take_order', user_id=call.from_user.id)),
        ]
        markup.add(*button)

        order_mes = await bot.send_message(chat_id=TOKEN.chatId, text="НОВЫЙ ЗАКАЗ!!!\n" + call.message.text + "\nНомер телефона - " + str(db.subscriber_exists(call.message.chat.id)[0][8]), reply_markup=markup)

        db.add_message_chat(message_chat=str(order_mes), order_id = str(db.get_order_last()[0][0]))

        markup_com = types.InlineKeyboardMarkup(row_width=1)
        button_1 = [
            # Реализовать функцию комментериев
            #types.InlineKeyboardButton(text='📃Добавить комментарий к заказу', callback_data=comment_data.new(action="add_comment", func="comment", id_db=str(db.get_order_last()[0][0]) )),
            types.InlineKeyboardButton(text="⭕️Отменить заказ", callback_data=comment_data.new(action="chanel_order", func="comment", id_db=str(db.get_order_last()[0][0]) ))
        ]
        markup_com.add(*button_1)
        client_mes= await bot.send_message(call.message.chat.id, text ="""🎉Ваш заказ принят!\n⏳Ожидайте дальнейшей информации, мы уже ищем водителя!""", reply_markup=markup_com)
        db.add_message_client(message_client=str(client_mes), order_id = str(db.get_order_last()[0][0]))

async def add_comment(call: CallbackData, callback_data:dict):
    id_db = callback_data.get('id_db')
    await bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = [
        types.InlineKeyboardButton(text='Отмена❌', callback_data=comment_data.new(action="chanel_comment", func="comment", id_db=id_db )),
        ]
    markup.add(*button)
    await bot.send_message(call.message.chat.id, text ="Пришлите текст одним сообщением", reply_markup=markup)
    await From.comment.set()

async def get_comment(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    await bot.edit_message_text(chat_id=TOKEN.chatId, message_id=json.loads(str(db.get_message_chat(message.from_user.id)))['message_id'], text=json.loads(str(db.get_message_chat(message.from_user.id)))['text'] + "\nКомментарий к заказу - " + message.text, reply_markup=json.loads(str(db.get_message_chat(message.from_user.id)))['reply_markup'])
    await bot.send_message(message.chat.id, text ="Комментарий добавлен")

async def chanel_cooment(call: CallbackData, callback_data:dict, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    # await bot.send_message(call.message.chat.id, text ="Задача отменена")

async def chanel_order(call: CallbackData, callback_data:dict):
    id_db = callback_data.get('id_db')
    db.add_finish_order(id_db)
    await bot.edit_message_text(chat_id=TOKEN.chatId, message_id=json.loads(str(db.get_message_chat(call.from_user.id)))['message_id'], text=json.loads(str(db.get_message_chat(call.from_user.id)))['text'] + "\nЗаказ отменён!")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=json.loads(str(db.get_message_client(call.from_user.id)))['message_id'], text=json.loads(str(db.get_message_client(call.from_user.id)))['text'] + "\nЗаказ отменён!")



def register_handler(dp: Dispatcher):
    dp.register_callback_query_handler(chanel_cooment, comment_data.filter(action=['chanel_comment']), state=From.comment)
    dp.register_message_handler(get_comment, state=From.comment)
    dp.register_callback_query_handler(add_comment,comment_data.filter(action=['add_comment']))
    dp.register_callback_query_handler(new_order, location_data.filter(func=['location']))
    dp.register_message_handler(location, commands = ['order'])
    dp.register_message_handler(get_location, content_types=types.ContentType.LOCATION)
    dp.register_callback_query_handler(chanel_order, comment_data.filter(action=['chanel_order']))
    # dp.register_callback_query_handler(chanel_order, comment_data.filter(action=['chanel_order']), state=From.comment)