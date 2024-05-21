import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import admin, handlers

from aiogram import Bot, Dispatcher

from config import config
from db import createtables


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config.bot_token.get_secret_value())


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(admin.router, handlers.router)
    await createtables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())