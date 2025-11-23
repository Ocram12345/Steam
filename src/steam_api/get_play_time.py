# Получение времени игры пользователя Steam по его SteamID и AppID игры
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения времени игры пользователя Steam по его SteamID и AppID игры
def get_play_time(api_key, steam_user_id, app_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_user_id}&format=json&include_played_free_games=1"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация об играх пользователя
        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            for game in games:
                if game['appid'] == app_id:
                    play_time = game.get('playtime_forever', 0)
                    logging.info(f"Время игры для Steam ID {steam_user_id} в игре AppID {app_id}: {play_time} минут.")
                    return play_time
            logging.info(f"Игра с AppID {app_id} не найдена для пользователя Steam ID {steam_user_id}.")
            return 0
        else:
            logging.info(f"У пользователя Steam ID {steam_user_id} нет игр или пользователь не существует.")
            return 0
    except Exception as e:
        logging.error(f"Ошибка при получении времени игры для Steam ID {steam_user_id} и AppID {app_id}: {e}")
        return 0
    
   
    
"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_play_time, которая принимает API-ключ Steam, SteamID пользователя и AppID игры.
4. Внутри функции формируется URL для запроса к Steam Web API, который получает список игр пользователя по его SteamID.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию об играх пользователя. Если да, происходит поиск игры с указанным AppID.
7. Если игра найдена, извлекается время игры (в минутах) и логируется. Если игра не найдена, логируется соответствующее сообщение.
8. Если у пользователя нет игр или пользователь не существует, логируется соответствующее сообщение.
9. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает 0.
"""