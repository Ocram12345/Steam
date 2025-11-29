# Команда для просмотра профиля пользователя в Steam используя базы данных
import sqlite3
import sys
import logging
from pathlib import Path
import dotenv
import os
from aiogram import Router, types
from aiogram.filters import Command

# Добавление пути к корневой директории проекта для корректного импорта модулей
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SRC_ROOT = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Импорт необходимых функций из steam и модулей базы данных
from steam.get_user_name import get_user_name
from telegram.sqlite_tg.sq_table_init import init_steam_users_table
from sqlite.sq_table_fill import SQLiteTableFiller
from sqlite.sq_table_init import initialize_tables
# Загрузка переменных окружения
dotenv.load_dotenv(PROJECT_ROOT / ".env")

# Путь к базе данных SQLite
DB_TELEGRAM_PATH = SRC_ROOT / "telegram" / "sqlite_tg" / "telegram_bot.db"
DB_STEAM_PATH = SRC_ROOT / "sqlite" / "steam_data.db"

# Гарантируем существование директорий баз данных
DB_TELEGRAM_PATH.parent.mkdir(parents=True, exist_ok=True)
DB_STEAM_PATH.parent.mkdir(parents=True, exist_ok=True)

# Загрузка переменных окружения
dotenv.load_dotenv()

# Получение Steam API ключа из переменных окружения
api_key = os.getenv("STEAM_API_KEY")

# Инициализация роутера
router = Router()


TELEGRAM_MESSAGE_LIMIT = 3800


def _iter_game_messages(games):
    lines = [
        f"{index + 1}. {game[0]}: {max((game[1] or 0) // 60, 0)} ч."
        for index, game in enumerate(games)
    ]

    chunk = []
    chunk_len = 0
    for line in lines:
        line_len = len(line) + 1  # newline separator
        if chunk and chunk_len + line_len > TELEGRAM_MESSAGE_LIMIT:
            yield "\n".join(chunk)
            chunk = []
            chunk_len = 0

        chunk.append(line)
        chunk_len += line_len

    if chunk:
        yield "\n".join(chunk)

# Обработчик команды /view_user_profile
@router.message(Command("view_user_profile"))
async def view_user_profile_command(message: types.Message):
    try:
        telegram_user_id = message.from_user.id

        # Убеждаемся, что таблица соответствия Telegram ↔ Steam ID инициализирована
        init_steam_users_table(DB_TELEGRAM_PATH)

        with sqlite3.connect(DB_TELEGRAM_PATH) as tg_conn:
            cursor = tg_conn.cursor()
            cursor.execute(
                "SELECT steam_id FROM steam_users WHERE telegram_user_id = ?",
                (telegram_user_id,),
            )
            result = cursor.fetchone()

        if not result:
            await message.answer(
                "Ваш SteamID не найден в базе данных. Пожалуйста, зарегистрируйте его с помощью команды /steam_profile."
            )
            return

        steam_user_id = result[0]

        # Обновляем локальную базу Steam свежими данными
        with sqlite3.connect(DB_STEAM_PATH) as steam_conn:
            initialize_tables(steam_conn)
            filler = SQLiteTableFiller(steam_conn, api_key)
            filler.fill_user_table(steam_user_id)
            filler.fill_game_table(steam_user_id)
            filler.fill_users_games_table(steam_user_id)

        # Получаем данные пользователя и его игры из базы
        with sqlite3.connect(DB_STEAM_PATH) as steam_conn:
            cursor = steam_conn.cursor()
            cursor.execute(
                "SELECT account_name FROM User WHERE id = ?",
                (steam_user_id,),
            )
            user_row = cursor.fetchone()

            if not user_row:
                await message.answer("Профиль пользователя не найден в базе данных Steam.")
                return

            account_name = user_row[0]

            cursor.execute(
                """
                SELECT Game.name, UsersGames.game_time
                FROM UsersGames
                JOIN Game ON UsersGames.game_id = Game.id
                WHERE UsersGames.user_id = ?
                ORDER BY UsersGames.game_time DESC
                """,
                (steam_user_id,),
            )
            games = cursor.fetchall()

        if not games:
            await message.answer(
                "В базе не найдено игр для вашего SteamID. Попробуйте обновить данные позже."
            )
            return

        header = (
            f"Профиль Steam пользователя:\n"
            f"Имя аккаунта: {account_name}\n"
            f"SteamID: {steam_user_id}\n"
            f"Количество игр: {len(games)}\n"
            f"Список игр:"
        )
        await message.answer(header)

        for chunk in _iter_game_messages(games):
            await message.answer(chunk)

    except Exception as exc:
        logging.error("Ошибка при обработке профиля пользователя: %s", exc)
        await message.answer("Произошла ошибка при проверке вашего SteamID в базе данных.")
