import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers import addshop, delshop, report, help, shops
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def set_commands():
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/addshop", description="Добавить магазин"),
        BotCommand(command="/delshop", description="Удалить магазин"),
        BotCommand(command="/shops", description="Список магазинов"),
        BotCommand(command="/report", description="Запросить отчет по продажам"),
        BotCommand(command="/help", description="Получить помощь по использованию бота"),
    ]
    await bot.set_my_commands(commands)


async def main():

    dp.include_router(addshop.router)
    dp.include_router(delshop.router)
    dp.include_router(report.router)
    dp.include_router(help.router)
    dp.include_router(shops.router)

    await set_commands()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
