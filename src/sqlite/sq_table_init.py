#Инициализация таблицы SQlite для хранения данных пользователей и игр
import logging

logger = logging.getLogger(__name__)


def initialize_tables(connection):
    """Создает таблицы базы данных, если они еще не существуют."""
    logger.info("Инициализация таблиц базы данных запущена.")
    # Создание таблицы пользователей
    connection.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY not null,
            account_name TEXT not null DEFAULT 'None')
    ''')

    logger.info("Таблица User создана.")

    # Создание таблицы игр
    connection.execute('''
        CREATE TABLE IF NOT EXISTS Game (
            id INTEGER PRIMARY KEY not null,
            name TEXT not null DEFAULT 'None')
    ''')

    logger.info("Таблица Game создана.")

    # Создание таблицы игр пользователей
    connection.execute('''
        CREATE TABLE IF NOT EXISTS UsersGames (
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            game_time INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, game_id),
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (game_id) REFERENCES Game(id))
    ''')

    logger.info("Таблица UsersGames создана.")

    connection.commit()
    
    logger.info("Инициализация таблиц базы данных завершена.")