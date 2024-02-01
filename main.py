
import asyncio
from aiogram import types 


from creat_bot import dp, bot, os

from Handlers.start import start, driver
from Handlers.task import order, trip
from Handlers.chat import chat_config
from Handlers.menu import menu
from Handlers.echo import echo

# postman.register_handler(dp)
start.register_handler_start(dp)
order.register_handler(dp)
trip.register_handler(dp)
driver.register_handler(dp)
chat_config.register_handler(dp)
menu.register_handler_menu(dp)
echo.register_handler_echo_bot(dp)

async def main():
    await dp.bot.set_my_commands([
        types.BotCommand("start", "📋 - Главное меню, перезаупстить бота."),
        types.BotCommand("order", "🆘 - Заказать такси."),
        types.BotCommand("menu", "Меню"),
        types.BotCommand("help", "Помощь. Справка."),
        types.BotCommand("reg_driver", "Стать водителем")
        ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
	
if __name__ == "__main__":
    asyncio.run(main())
    