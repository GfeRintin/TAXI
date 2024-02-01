from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from creat_bot import dp, bot, db, TOKEN, os
from Handlers.task.order import order_id_data, From
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import json





async def take_order(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('user_id')
    order_id_call = callback_data.get("id_db")

    if bool(call.from_user.username):
        if call.from_user.username == db.subscriber_exists(call.from_user.id)[0][2]:
            pass
        else:
            db.update_UserName(call.from_user.id, call.from_user.username)
    else:
        pass




    #проверяем нет ли не завершённого заказа
    if db.order_finish__exists(call.from_user.username) != None:
        await call.answer("Вы ещё не завершили предыдущий заказ", show_alert=True)
        return
        



    markup = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text='Приехал✅', callback_data=order_id_data.new(id_db=order_id_call, func="arrived",user_id=user_id)),
        ]
    markup.add(*button)
    db.get_order(order_id=order_id_call, username = str(db.subscriber_exists(call.from_user.id)[0][2]))
    
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= call.message.text + "\nЗаказ взял - " + str(db.subscriber_exists(call.from_user.id)[0][3]) + " (" + str(db.subscriber_exists(call.from_user.id)[0][2]) + ")", reply_markup=markup)
    await bot.delete_message(chat_id=user_id, message_id=json.loads(str(db.get_message_client(user_id)))['message_id'])

    PATH = os.getcwd()
    src = PATH + "\\DB\\car\\" + str(db.subscriber_exists(call.from_user.id)[0][10]) + ".png"
    with open(src, 'rb') as photo:
        await bot.send_photo(chat_id=user_id, caption=json.loads(str(db.get_message_client(user_id)))['text'] + "\nВаш заказ приняли, придет - " + str(db.subscriber_exists(call.from_user.id)[0][10]), photo=photo)
                           
async def arrived(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('user_id')
    order_id_call = callback_data.get("id_db")
    
    #Проверка этого ли водителя заказ
    if db.order_who_get_order__exists(order_id_call) == call.from_user.username:
        pass
    else:
        await call.answer("Это не ваш заказ!!!", show_alert=True)
        return

    db.add_arrived_order(order_id_call)

    #Сообщение в чат
    markup_finish = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text='Завершить заказ🏁', callback_data=order_id_data.new(id_db=order_id_call, func="finish_order",user_id=user_id)),
        ]
    markup_finish.add(*button)
    order_mes = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= call.message.text + "\nВы приехали!", reply_markup=markup_finish)
    db.add_message_chat(message_chat=str(order_mes), order_id=order_id_call)

    #Сообщение клиенту
    markup_leave = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text='Выхожу✅', callback_data=order_id_data.new(id_db=order_id_call, func="leave",user_id=user_id)),
        ]
    markup_leave.add(*button)
    mes_client = await bot.send_message(chat_id=user_id, text="Водитель прибыл, ожидание 5 минут", reply_markup=markup_leave)
    db.add_message_client(str(mes_client), order_id_call)

async def leave(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('user_id')
    order_id_call = callback_data.get("id_db")

    #Сообщение в чат
    await bot.edit_message_text(chat_id=TOKEN.chatId, message_id=json.loads(str(db.get_message_chat(user_id)))['message_id'], text= json.loads(str(db.get_message_chat(user_id)))['text'] + "\nЗаказчики уже выходят!", reply_markup=json.loads(str(db.get_message_chat(user_id)))['reply_markup'])
    #Сообщение клиенту
    await bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="\nОтлично, мы сообщили об этом водителю")

async def finish_order(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('user_id')
    order_id_call = callback_data.get("id_db")

    #Проверка этого ли водителя заказ
    if db.order_who_get_order__exists(order_id_call) == call.from_user.username:
        pass
    else:
        await call.answer("Это не ваш заказ!!!", show_alert=True)
        return
    

    
    

    # Сообщение в чат
    await bot.edit_message_text(chat_id=TOKEN.chatId, message_id=call.message.message_id , text= call.message.text + "\nВы завершили заказ!")

    # Сообщение клиенту
    await bot.delete_message(chat_id=user_id, message_id=json.loads(str(db.get_message_client(user_id)))['message_id'])
    await bot.send_message(chat_id=user_id, text="""✅Ваш заказ был успешно выполнен!\n🙌Благодарим вас за выбор нашей компании! Надеемся, что вы остались довольны нашим сервисом!""")


    # Отметка в бд минус заказ
    db.add_finish_order(order_id_call)
    db.add_finish_order_diver(call.from_user.id)
    db.add_finish_order_client(user_id)
    if db.get_orders_left(call.from_user.id)[0] == 0:
        await call.answer("У вас закончились заказы, вы будете удалены из чата. Чтобы вновь пользоваться зарегистрируйтесь как водитель", show_alert=True)
        await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id)




def register_handler(dp: Dispatcher):
    dp.register_callback_query_handler(take_order, order_id_data.filter(func=['take_order']))
    dp.register_callback_query_handler(arrived, order_id_data.filter(func=['arrived']))
    dp.register_callback_query_handler(leave, order_id_data.filter(func=['leave']))
    dp.register_callback_query_handler(finish_order, order_id_data.filter(func=['finish_order']))
    # dp.register_message_handler(location, commands = ['trip'])
    # dp.register_message_handler(get_location, content_types=types.ContentType.LOCATION)