# Заполнение таблиц базы данных SQLite данными из Steam API
import sqlite3
import sys
from dotenv import load_dotenv
import os
import logging


# Обеспечить возможность импорта пакета steam при прямом запуске файла.
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from sqlite.sq_table_init import initialize_tables
from steam.get_owned_games import get_owned_games
from steam.get_user_name import get_user_name
from steam.is_real_user import is_real_user


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Класс для заполнения таблиц базы данных SQLite данными из Steam API
class SQLiteTableFiller():
    # Инициализация с соединением к базе данных и API-ключом Steam
    def __init__(self, connection, api_key):
        self.connection = connection
        self.api_key = api_key
    # Заполнение таблицы User информацией о пользователе Steam
    def fill_user_table(self, steam_user_id):
        logging.info("Заполнение таблицы User запущено.")
        account_name = get_user_name(self.api_key, steam_user_id)
        if not account_name:
            raise RuntimeError(f"Не удалось получить имя пользователя для Steam ID {steam_user_id}.")
        with self.connection:
            self.connection.execute(
                "INSERT OR IGNORE INTO User (id, account_name) VALUES (?, ?)",
                (steam_user_id, account_name),
            )
        logging.info("Заполнение таблицы User завершено.")
        
    # Заполнение таблицы Game информацией об играх пользователя Steam
    def fill_game_table(self, steam_user_id, owned_games=None):
        logging.info("Заполнение таблицы Game запущено.")
        games = owned_games if owned_games is not None else get_owned_games(self.api_key, steam_user_id)
        if not games:
            logging.warning("Список игр пуст. Возможно, игры скрыты или произошла ошибка при запросе.")
            return

        with self.connection:
            for game in games:
                game_id = game.get("appid")
                if game_id is None:
                    logging.warning("Пропуск записи без appid: %s", game)
                    continue
                game_name = game.get("name") or "None"
                self.connection.execute(
                    """
                    INSERT INTO Game (id, name) VALUES (?, ?)
                    ON CONFLICT(id) DO UPDATE SET name=excluded.name
                    """,
                    (game_id, game_name),
                )
                logging.info("Добавлена/обновлена игра с id %s", game_id)
        logging.info("Заполнение таблицы Game завершено.")
    # Заполнение таблицы UsersGames информацией о времени игры пользователя в каждую игру
    def fill_users_games_table(self, steam_user_id, owned_games=None):
        logging.info("Заполнение таблицы UsersGames запущено.")
        games = owned_games if owned_games is not None else get_owned_games(self.api_key, steam_user_id)
        if not games:
            logging.warning("Не удалось получить игры пользователя при заполнении UsersGames.")
            return

        with self.connection:
            for game in games:
                game_id = game.get("appid")
                if game_id is None:
                    continue
                play_time = int(game.get("playtime_forever", 0))
                self.connection.execute(
                    """
                    INSERT INTO UsersGames (user_id, game_id, game_time)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, game_id) DO UPDATE SET game_time=excluded.game_time
                    """,
                    (steam_user_id, game_id, play_time),
                )
        logging.info("Заполнение таблицы UsersGames завершено.")
        
    # Заполнение списка игр пользователя с указанием времени игры
    def fill_user_games(self, steam_user_id):
        logging.info("Получение игр пользователя запущено.")
        user_exists = self.connection.execute(
            "SELECT 1 FROM User WHERE id = ?", (steam_user_id,)
        ).fetchone()
        if not user_exists:
            raise RuntimeError(f"Пользователь с Steam ID {steam_user_id} не найден в базе данных.")

        user_games = self.connection.execute(
            """
            SELECT g.name, ug.game_time
            FROM UsersGames ug
            JOIN Game g ON ug.game_id = g.id
            WHERE ug.user_id = ?
            ORDER BY ug.game_time DESC
            """,
            (steam_user_id,),
        ).fetchall()

        user_name_row = self.connection.execute(
            "SELECT account_name FROM User WHERE id = ?", (steam_user_id,)
        ).fetchone()
        user_name = user_name_row[0] if user_name_row else "<unknown>"

        if not user_games:
            logging.info("У пользователя %s отсутствуют сохраненные игры в базе.", user_name)
            return

        for index, game in enumerate(user_games, start=1):
            hours_played = (game[1] or 0) / 60
            logging.info(
                "%d) Игра пользователя %s: %s, Время игры: %.2fh",
                index,
                user_name,
                game[0] or "<unknown>",
                hours_played,
            )
        logging.info("Получение игр пользователя завершено.")



# Проверка и заполнение базы данных при запуске скрипта
"""if __name__ == "__main__":
    if not API_KEY:
        logging.error("Переменная окружения STEAM_API_KEY не задана.")
        sys.exit(1)

    if not STEAM_USER_ID:
        logging.error("Переменная окружения STEAM_USER_ID не задана.")
        sys.exit(1)

    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")

    initialize_tables(connection)

    filler = SQLiteTableFiller(connection, API_KEY)

    if not is_real_user(API_KEY, STEAM_USER_ID):
        logging.error("Пользователь с Steam ID %s не существует или его игры скрыты.", STEAM_USER_ID)
        connection.close()
        sys.exit(1)

    try:
        filler.fill_user_table(STEAM_USER_ID)
        owned_games = get_owned_games(API_KEY, STEAM_USER_ID)
        filler.fill_game_table(STEAM_USER_ID, owned_games=owned_games)
        filler.fill_users_games_table(STEAM_USER_ID, owned_games=owned_games)
        filler.fill_user_games(STEAM_USER_ID)
    except (sqlite3.DatabaseError, RuntimeError) as exc:
        logging.error("Ошибка при заполнении базы данных: %s", exc)
        sys.exit(1)
    finally:
        connection.close()"""

    
  
"""
Как работает этот код:
1. Импортируются необходимые модули, включая sqlite3 для работы с базой данных SQLite, sys для управления выходом из программы, dotenv для загрузки переменных окружения и logging для логирования.
2. Настраивается логирование на уровень INFO.
3. Загружаются переменные окружения из файла .env, включая API-ключ Steam, SteamID пользователя и имя базы данных.
4. Определяется класс SQLiteTableFiller, который содержит методы для заполнения таблиц базы данных SQLite данными из Steam API:
   - fill_user_table: Заполняет таблицу User информацией о пользователе Steam.
   - fill_game_table: Заполняет таблицу Game информацией об играх пользователя Steam.
    - fill_users_games_table: Заполняет таблицу UsersGames информацией о времени игры пользователя в каждую игру.
    - fill_user_games: Логирует список игр пользователя с указанием времени игры.
5. В блоке if __name__ == "__main__": проверяется наличие необходимых переменных окружения и устанавливается соединение с базой данных SQLite.
6. Инициализируются таблицы базы данных с помощью функции initialize_tables.
7. Создается экземпляр класса SQLiteTableFiller и проверяется существование пользователя Steam с помощью функции is_real_user.
8. Если пользователь существует, вызываются методы класса SQLiteTableFiller для заполнения таблиц базы данных и логирования игр пользователя.
9. В случае возникновения ошибок при заполнении базы данных, ошибки логируются, и программа завершается с кодом ошибки.
10. В блоке finally соединение с базой данных закрывается.
"""