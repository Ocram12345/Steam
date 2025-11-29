# Получение достижений для конкретной игры пользователя Steam по его SteamID
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def get_achievements_for_usergame(api_key, steam_user_id, app_id, language="english"):
    """Возвращает названия полученных достижений и их количество для указанной игры."""
    try:
        url = (
            "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
            f"?key={api_key}&steamid={steam_user_id}&appid={app_id}&l={language}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as request_error:
        logging.error(
            "Игра под AppID: %s для пользователя не найдена %s: %s",
            app_id,
            steam_user_id,
            request_error,
        )
        return {"names": [], "count": 0}

    try:
        data = response.json()
    except ValueError:
        logging.error(
            "Ответ Steam API по достижениям не является JSON (app %s, user %s).",
            app_id,
            steam_user_id,
        )
        return {"names": [], "count": 0}

    player_stats = data.get("playerstats", {})
    achievements = player_stats.get("achievements", [])
    unlocked_names = []

    for achievement in achievements:
        if achievement.get("achieved") == 1:
            name = achievement.get("name") or achievement.get("apiname")
            if name:
                unlocked_names.append(name)

    if not unlocked_names:
        logging.info(
            "Полученные достижения для пользователя %s и игры %s отсутствуют.",
            steam_user_id,
            app_id,
        )
    else:
        logging.info(
            "Получено %s достижений для пользователя %s в игре %s.",
            len(unlocked_names),
            steam_user_id,
            app_id,
        )

    return {"names": unlocked_names, "count": len(unlocked_names)}
    
    
    
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