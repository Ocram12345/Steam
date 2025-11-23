# Тесты для проверки работы всех функций steam_api
import os
import sys
import unittest
from dotenv import load_dotenv

# Обеспечить возможность импорта пакета steam_api при прямом запуске файла теста (By AI)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Импорт всех функций из steam_api для тестирования
from steam_api.get_achievements_for_usergame import get_achievements_for_usergame
from steam_api.get_owned_games import get_owned_games
from steam_api.get_play_time import get_play_time
from steam_api.is_real_user import is_real_user
from steam_api.get_user_name import get_user_name
from steam_api.get_game_name import get_game_name
from steam_api.get_friend_list import get_friend_list


# Загрузка переменных окружения из файла .env
load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")
TEST_STEAM_USER_ID = os.getenv("STEAM_USER_ID")

# Тестовый AppID
TEST_APP_ID = 1091500  # Пример AppID для тестирования (Cyberpunk 2077)

# Тесты для всех функций steam_api
class TestSteamAPI(unittest.TestCase):

    # Проверка на существование пользователя Steam по его SteamID
    def test_is_real_user(self):
        result = is_real_user(API_KEY, TEST_STEAM_USER_ID)
        self.assertTrue(result)
        
    # Получение списка игр пользователя Steam по его SteamID
    def test_get_owned_games(self):
        games = get_owned_games(API_KEY, TEST_STEAM_USER_ID)
        self.assertIsInstance(games, list)
        
    # Получение достижений для конкретной игры пользователя Steam по его SteamID
    def test_get_achievements_for_usergame(self):
        achievements = get_achievements_for_usergame(API_KEY, TEST_STEAM_USER_ID, TEST_APP_ID)
        self.assertIsInstance(achievements, list)
        
    # Получение времени игры пользователя Steam по его SteamID и AppID игры
    def test_get_play_time(self):
        play_time = get_play_time(API_KEY, TEST_STEAM_USER_ID, TEST_APP_ID)
        self.assertIsInstance(play_time, int)
        
    # Получение имени пользователя Steam по его SteamID
    def test_get_user_name(self):
        user_name = get_user_name(API_KEY, TEST_STEAM_USER_ID)
        self.assertIsInstance(user_name, str)
        
    # Получение названия игры по ее AppID
    def test_get_game_name(self):
        game_name = get_game_name(API_KEY, TEST_APP_ID)
        self.assertIsInstance(game_name, str)
        
    # Получение списка друзей пользователя Steam по его SteamID
    def test_get_friend_list(self):
        friends = get_friend_list(API_KEY, TEST_STEAM_USER_ID)
        self.assertIsInstance(friends, list)

# Запуск тестов
if __name__ == "__main__":
    unittest.main()
    


"""
Этот код представляет собой набор тестов для проверки работы различных функций, взаимодействующих с Steam API. Вот как он работает:
1. Импортируются необходимые модули, включая os, sys, unittest и функции из steam_api.
2. Добавляется путь к steam_api в sys.path, чтобы обеспечить возможность импорта при запуске тестового файла напрямую.
3. Загружаются переменные окружения из файла .env с помощью dotenv, включая API-ключ Steam.
4. Определяется класс TestSteamAPI, наследующий от unittest.TestCase, который содержит методы для тестирования каждой функции из steam_api.
5. Каждый метод теста вызывает соответствующую функцию из steam_api с тестовыми данными и проверяет тип возвращаемого значения с помощью assertIsInstance или assertTrue.
6. В конце файла вызывается unittest.main(), чтобы запустить все тесты при выполнении скрипта.
Этот набор тестов помогает убедиться, что функции steam_api работают корректно и возвращают ожидаемые типы данных при взаимодействии с Steam API.
"""
