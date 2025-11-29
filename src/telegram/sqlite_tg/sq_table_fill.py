# Заполнение таблиц базы данных SQLite для Telegram-бота
import sqlite3
def fill_steam_users_table(db_path: str, user_data: list):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executemany("""
    INSERT OR REPLACE INTO steam_users (telegram_user_id, steam_id)
    VALUES (?, ?)
    """, user_data)
    
    conn.commit()
    conn.close()