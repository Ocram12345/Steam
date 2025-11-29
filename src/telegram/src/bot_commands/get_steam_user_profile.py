# Получение Steam_ID профиля пользователя Steam по его URL или имени пользователя и сохранение в базу данных
import sys
import logging
from pathlib import Path
import dotenv
import os
from aiogram import Router, types
from aiogram.filters import Command

# Добавление пути к корневой директории проекта для корректного импорта модулей
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

# Импорт необходимых функций из steam
from steam.get_user_id import get_user_id
from telegram.sqlite_tg.sq_table_init import init_steam_users_table
from telegram.sqlite_tg.sq_table_fill import fill_steam_users_table

# Загрузка переменных окружения
dotenv.load_dotenv(PROJECT_ROOT / ".env")

# Путь к базе данных SQLite
DB_PATH = PROJECT_ROOT / "telegram" / "sqlite_tg" / "telegram_bot.db"
# Загрузка переменных окружения
dotenv.load_dotenv()
# Получение Steam API ключа из переменных окружения
api_key = os.getenv("STEAM_API_KEY")
# Инициализация роутера
router = Router()
# Обработчик команды /steam_profile
@router.message(Command("steam_profile"))
async def get_steam_user_profile_command(message: types.Message):
    try:
        # Извлечение Steam профиля из сообщения
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Пожалуйста, укажите URL профиля Steam или имя пользователя после команды.")
            return

        profile_input = args[1]

        # Получение SteamID
        steam_user_id = get_user_id(profile_input, api_key)
        if not steam_user_id:
            await message.answer("Не удалось получить SteamID. Пожалуйста, проверьте введённые данные.")
            return

        # Инициализация таблицы в базе данных, если она не существует
        init_steam_users_table(DB_PATH)

        # Сохранение связи между Telegram user_id и SteamID в базу данных
        telegram_user_id = message.from_user.id
        fill_steam_users_table(DB_PATH, [(telegram_user_id, steam_user_id)])

        await message.answer(f"Ваш SteamID {steam_user_id} успешно сохранён в базе данных.")

    except Exception as e:
        logging.error("Ошибка при обработке команды get_steam_user_profile: %s", e)
        await message.answer("Произошла ошибка при обработке вашего запроса.")
