# Получение имени пользователя Steam по его SteamID
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения имени пользователя Steam по его SteamID
def get_user_name(api_key, steam_user_id):
    try:
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_user_id}"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация о пользователе
        if 'response' in data and 'players' in data['response'] and len(data['response']['players']) > 0:
            user_name = data['response']['players'][0]['personaname']
            logging.info(f"Имя пользователя для Steam ID {steam_user_id}: {user_name}.")
            return user_name
        else:
            logging.info(f"Пользователь с Steam ID {steam_user_id} не найден.")
            return None
    except Exception as e:
        logging.error(f"Ошибка при получении имени пользователя для Steam ID {steam_user_id}: {e}")
        return None



"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_user_name, которая принимает API-ключ Steam и SteamID пользователя.
4. Внутри функции формируется URL для запроса к Steam Web API, который получает информацию о пользователе по его SteamID.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию о пользователе. Если да, извлекается имя пользователя и логируется его. Если нет, логируется сообщение о том, что пользователь не найден.
7. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает None.
"""