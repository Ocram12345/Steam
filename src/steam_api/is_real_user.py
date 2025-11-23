#Проверка на существование пользователя Steam по его SteamID
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция проверки существования пользователя Steam по его SteamID
def is_real_user(api_key, steam_user_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_user_id}&format=json"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация об играх пользователя
        if 'response' in data and 'games' in data['response']:
            logging.info(f"Пользователь Steam ID {steam_user_id} существует.")
            return True
        else:
            logging.info(f"Пользователь Steam ID {steam_user_id} не существует.")
            return False
    except Exception as e:
        logging.error(f"Ошибка при проверке Steam ID {steam_user_id}: {e}")
        return False



"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования, requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция is_real_user, которая принимает API-ключ Steam и SteamID пользователя.
4. Внутри функции формируется URL для запроса к Steam Web API, который пытается получить список игр пользователя.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию об играх пользователя. Если да, логируется сообщение о существовании пользователя и возвращается True. Если нет, логируется сообщение о несуществовании пользователя и возвращается False.
7. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает False.
"""