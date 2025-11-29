#Получение списка игр пользователя Steam по его SteamID
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения списка игр пользователя Steam по его SteamID
def get_owned_games(api_key, steam_user_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_user_id}&format=json&include_appinfo=1"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация об играх пользователя
        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            logging.info(f"Получено {len(games)} игр для пользователя Steam ID {steam_user_id}.")
            return games
        else:
            logging.info(f"У пользователя Steam ID {steam_user_id} нет игр или пользователь не существует.")
            return []
    except Exception as e:
        logging.error(f"Ошибка при получении игр для Steam ID {steam_user_id}: {e}")
        return []
    


"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_owned_games, которая принимает API-ключ Steam и SteamID пользователя.
4. Внутри функции формируется URL для запроса к Steam Web API, который получает список игр пользователя.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию об играх пользователя. Если да, то извлекается список игр и логируется количество полученных игр. Если нет, логируется сообщение о том, что у пользователя нет игр или он не существует.
7. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает пустой список.
"""