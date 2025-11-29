import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import logging
from dotenv import load_dotenv

from bot_commands import start, help, get_steam_user_profile, view_user_profile


# Получиние токена бота из переменных окружения
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка наличия токена бота
if not bot_token:
    raise RuntimeError(
        "Environment variable TELEGRAM_BOT_TOKEN is missing; set your bot token before starting the bot."
    )

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
SteamBOT = Bot(token=bot_token)
dp = Dispatcher()

# Регистрация роутеров команд
dp.include_router(start.router)
dp.include_router(help.router)  
dp.include_router(get_steam_user_profile.router)
dp.include_router(view_user_profile.router)
# Запуск бота
async def main():
    await dp.start_polling(SteamBOT)

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())
        
