# Получение достидений для конкретной игры пользователя Steam по его SteamID
import logging  
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения достижений для конкретной игры пользователя Steam по его SteamID
def get_achievements_for_usergame(api_key, steam_user_id, app_id):
    try:
        url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?key={api_key}&steamid={steam_user_id}&appid={app_id}"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация о достижениях пользователя для игры
        if 'playerstats' in data and 'achievements' in data['playerstats']:
            achievements = data['playerstats']['achievements']
            logging.info(f"Получено {len(achievements)} достижений для пользователя Steam ID {steam_user_id} в игре AppID {app_id}.")
            return achievements
        else:
            logging.info(f"Достижения для пользователя Steam ID {steam_user_id} в игре AppID {app_id} не найдены.")
            return []
    except Exception as e:
        logging.error(f"Ошибка при получении достижений для Steam ID {steam_user_id} в игре AppID {app_id}: {e}")
        return []
    
    
    
"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_achievements_for_usergame, которая принимает API-ключ Steam, SteamID пользователя и AppID игры.
4. Внутри функции формируется URL для запроса к Steam Web API, который получает достижения пользователя для конкретной игры по его SteamID.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию о достижениях пользователя для игры. Если да, извлекается список достижений и логируется их количество. Если нет, логируется сообщение о том, что достижения не найдены.
7. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает пустой список.
"""