from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from creat_bot import dp, bot, db, TOKEN, os
from Handlers.echo.check_reg import check_reg

from datetime import datetime, timedelta

driver_data=CallbackData("none", "action", "func", "user_id")

class From(StatesGroup):
    msg1 = State()
    msg2 = State()


async def reg_driver(message: types.Message):
    if not await check_reg(message):
        return
    if not bool(message.from_user.username):
        await bot.send_message(chat_id=message.chat.id, text="Чтобы стать водителем нужно добавить себе @username в телеграме")

    await bot.send_message(chat_id=message.chat.id, text="""👋 Приветствую вас, уважаемый водитель! 🚗

Добро пожаловать в нашу команду! Мы очень рады, что вы выбрали нашу платформу для предоставления услуг.

Для обеспечения высокого качества сервиса и безопасного путешествия наших клиентов, просим вас ознакомиться с некоторыми правилами:

1️⃣ Будьте вежливы и профессиональны во всех общениях с клиентами. Отзывы и репутация очень важны для нас.

2️⃣ Предоставляйте комфортную и безопасную поездку. Держите автомобиль в чистоте и исправности, соблюдая правила дорожного движения.

3️⃣ Уважайте личные границы клиентов и их конфиденциальность. Соблюдайте правила конфиденциальности и не раскрывайте личную информацию.

4️⃣ Будьте пунктуальны и надежны. Подтверждайте заказы вовремя и прибывайте к месту подачи автомобиля надлежащим образом.

5️⃣ Работайте с улыбкой и позитивным настроем. Личное обслуживание и дружелюбное отношение к клиентам являются нашей главной ценностью.

В случае возникновения вопросов или проблем, обратитесь к нашей службе поддержки, мы всегда готовы помочь.

Спасибо за ваше сотрудничество и желаем вам приятной и успешной работы! 🌟🚖""")
    await bot.send_message(chat_id=message.chat.id, text="Если вы готовы продолжить регистрацию, отправь номер своей машины в формате А123БВ123")
    await From.msg1.set()

async def reg_number_car(message: types.Message, state: FSMContext):
    number_car=message.text
    await state.finish()

    if len(number_car) > 9:
        await bot.send_message(chat_id=message.chat.id, text="Символов больше чем нужно")
        return
    if not number_car[0].isalpha():
        await bot.send_message(chat_id=message.chat.id, text="1неверный формат")
        return
    if not number_car[1].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="2неверный формат")
        return
    if not number_car[2].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="3неверный формат")
        return
    if not number_car[3].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="4неверный формат")
        return
    if not number_car[4].isalpha():
        await bot.send_message(chat_id=message.chat.id, text="5неверный формат")
        return
    if not number_car[5].isalpha():
        await bot.send_message(chat_id=message.chat.id, text="6неверный формат")
        return
    if not number_car[6].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="7неверный формат")
        return
    if not number_car[7].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="8неверный формат")
        return
    if not number_car[8].isdigit():
        await bot.send_message(chat_id=message.chat.id, text="9неверный формат")
        return
    
    #Добавление в БД
    db.add_number_car(number_car=number_car, user_id=message.from_user.id)
    await bot.send_message(chat_id=message.chat.id, text="Отлично!\nПришли одно фото машины,где отчётливо видно номера")
    await From.msg2.set()

async def reg_photo_car(message: types.Message, state: FSMContext):
    if not message.content_type == 'photo':
        await bot.send_message(chat_id=message.chat.id, text="Отправьте пожалуйста ОДНО фото")
        return
    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text="Отлично, ожидайте проверки администраторов, если вы проёдете проверку, то вас добавят в бесседу")

    # Скачивание фото
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    PATH = os.getcwd()
    src = PATH + "\\DB\\car\\" + str(db.give_number_car(message.from_user.id)) + ".png"
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())



    #Отправка водителя админу
    markup = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text='✅', callback_data=driver_data.new(action=True, func="new_driver", user_id=message.from_user.id)),
        types.InlineKeyboardButton(text='❌', callback_data=driver_data.new(action=False, func="new_driver", user_id=message.from_user.id)),
        types.InlineKeyboardButton(text=message.from_user.username, url='https://t.me/' + message.from_user.username),

        ]
    markup.add(*button)
    with open(src, 'rb') as photo:
        await bot.send_photo(chat_id=TOKEN.adminChatId, photo=photo, caption="Принять ли нового водителя?\n " + str(db.give_number_car(message.from_user.id)), reply_markup=markup, parse_mode='HTML')


async def quantity_orders(call: CallbackData, callback_data: dict):
    """Выдаем колличество заказов"""
    user_id =callback_data.get("user_id")
    if callback_data.get("action") == "True":
        
        markup = types.InlineKeyboardMarkup()
        button = [
        types.InlineKeyboardButton(text='10', callback_data=driver_data.new(action=10, func="quantity", user_id=user_id)),
        types.InlineKeyboardButton(text='15', callback_data=driver_data.new(action=15, func="quantity", user_id=user_id)),
        types.InlineKeyboardButton(text='20', callback_data=driver_data.new(action=20, func="quantity", user_id=user_id)),
        types.InlineKeyboardButton(text='25', callback_data=driver_data.new(action=25, func="quantity", user_id=user_id)),
        types.InlineKeyboardButton(text='30', callback_data=driver_data.new(action=30, func="quantity", user_id=user_id)),
        ]
        markup.add(*button)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=str(call.message.caption) + "\nВыберите колличество заказов, которые вы ему выделите", reply_markup=markup)

    if callback_data.get("action") == "False":
        # Не Принял водителя
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=str(call.message.caption) + "\nВы не приняли водителя")
        await bot.send_message(chat_id=callback_data.get("user_id"), text="К сожалению Вас не приняли в водителей\n")

async def add_new_drive(call: CallbackData, callback_data: dict):
        """Принимаем водителя"""        
        # Принял водителя
        db.add_driver(callback_data.get("user_id"), int(callback_data.get("action")))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=str(call.message.caption) + "\nВы приняли водителя")
        expire_date = datetime.now() + timedelta(days=1)
        link = await bot.create_chat_invite_link(TOKEN.chatId, expire_date.timestamp, 1)
        await bot.send_message(chat_id=callback_data.get("user_id"), text="Вас приняли в водителей\n" + link.invite_link)
        

        


def register_handler(dp: Dispatcher):
    dp.register_callback_query_handler(quantity_orders, driver_data.filter(func=['new_driver']))
    dp.register_callback_query_handler(add_new_drive, driver_data.filter(func=['quantity']))
    dp.register_message_handler(reg_driver, commands=['reg_driver'])
    dp.register_message_handler(reg_number_car, state=From.msg1)
    dp.register_message_handler(reg_photo_car, content_types=types.ContentTypes.PHOTO, state=From.msg2)