from aiogram import types, Dispatcher 
from creat_bot import bot, db
from Handlers.start import updateUserName as uun
from Handlers.task.order import location
from aiogram.utils.callback_data import CallbackData


menu_data = CallbackData('none', 'action', 'func')

async def menu_call(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await menu(call.message)

async def menu(message: types.Message):

    uun.updateUserName(message)
    markup = types.InlineKeyboardMarkup(row_width=1)

    if db.driver_exists(message.chat.id):
        markup.add(types.InlineKeyboardButton(text='🚕Личный кабинет водителя', callback_data=menu_data.new(action='lk_driver', func='menu')),)
    
    button = [
        types.InlineKeyboardButton(text='🆘 - Заказать такси', callback_data=menu_data.new(action='order', func='menu')),
        types.InlineKeyboardButton(text='Помощь. Справка.', callback_data=menu_data.new(action='help', func='menu')),
        ]
    markup.add(*button)
    await bot.send_message(message.chat.id, text = 'Выбери действие⬇️', reply_markup = markup)

async def order(call:types.CallbackQuery):
    await location(call.message)

async def lk_driver(call:types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = [
        types.InlineKeyboardButton(text='Узнать сколько заказов осталось', callback_data=menu_data.new(action='orders_left', func='menu')),
        types.InlineKeyboardButton(text='Помощь. Справка. для водителя', callback_data=menu_data.new(action='help_diver', func='menu')),
        types.InlineKeyboardButton(text='Вернуться в меню↩️', callback_data=menu_data.new(action='menu', func='menu')),
        ]
    markup.add(*button)
    await bot.send_message(call.message.chat.id, text = 'Личный кабинет водителя-> Выбери действие⬇️', reply_markup=markup)


async def orders_left(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, text = "Осталось - " + str(db.orders_left(call.from_user.id)) + " заказов")

def register_handler_menu(dp: Dispatcher):
    dp.register_message_handler(menu, commands = ['menu'])
    dp.register_callback_query_handler(menu_call,menu_data.filter(action=['menu']))
    dp.register_callback_query_handler(order,menu_data.filter(action=['order']))
    dp.register_callback_query_handler(lk_driver,menu_data.filter(action=['lk_driver']))
    dp.register_callback_query_handler(orders_left, menu_data.filter(action=['orders_left']))