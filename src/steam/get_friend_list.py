# Получение списка друзей пользователя Steam по его SteamID
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения списка друзей пользователя Steam по его SteamID
def get_friend_list(api_key, steam_user_id):
    try:
        url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_user_id}&relationship=friend"
        response = requests.get(url)
        data = response.json()
        # Проверяем, есть ли в ответе информация о друзьях пользователя
        if 'friendslist' in data and 'friends' in data['friendslist']:
            friends = data['friendslist']['friends']
            logging.info(f"Получено {len(friends)} друзей для пользователя Steam ID {steam_user_id}.")
            return friends
        else:
            logging.info(f"У пользователя Steam ID {steam_user_id} нет друзей или пользователь не существует.")
            return []
    except Exception as e:
        logging.error(f"Ошибка при получении друзей для Steam ID {steam_user_id}: {e}")
        return []
# Функция получения списка SteamID друзей пользователя Steam по его SteamID
def get_friend_id_list(api_key, steam_user_id):
    friends = get_friend_list(api_key, steam_user_id)
    friend_ids = [friend['steamid'] for friend in friends]
    return friend_ids

"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_friend_list, которая принимает API-ключ Steam и SteamID пользователя.
4. Определяется функция get_friend_id_list, которая возвращает список SteamID друзей пользователя.
5. Внутри функции get_friend_list формируется URL для запроса к Steam Web API, который получает список друзей пользователя.
6. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
7. Проверяется, содержит ли ответ информацию о друзьях пользователя. Если да, извлекается список друзей и логируется их количество. Если нет, логируется сообщение о том, что у пользователя нет друзей или он не существует.
8. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает пустой список.
"""