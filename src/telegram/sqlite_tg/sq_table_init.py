# Создание таблицы для хранения Steam_ID и связи с Telegram user_id
import sqlite3

# Инициализация таблицы steam_users в базе данных SQLite
def init_steam_users_table(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS steam_users (
        telegram_user_id INTEGER PRIMARY KEY,
        steam_id TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
