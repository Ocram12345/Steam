# Получение названия игры по ее AppID в Steam
import logging
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения названия игры по ее AppID в Steam
def get_game_name(api_key, app_id):
    """Возвращает название игры по ее AppID, используя публичное API магазина Steam."""
    try:
        params = {"appids": app_id}
        response = requests.get("https://store.steampowered.com/api/appdetails", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        app_key = str(app_id)
        if app_key in data and data[app_key].get("success") and "data" in data[app_key]:
            game_name = data[app_key]["data"].get("name")
            if game_name:
                logging.info(f"Название игры для AppID {app_id}: {game_name}.")
                return game_name
        logging.info(f"Игра с AppID {app_id} не найдена.")
        return None
    except requests.RequestException as e:
        logging.error(f"Ошибка HTTP при получении названия игры для AppID {app_id}: {e}")
        return None
    except ValueError as e:
        logging.error(f"Ошибка разбора ответа для AppID {app_id}: {e}")
        return None
    


"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_game_name, которая принимает API-ключ Steam и AppID игры.
4. Внутри функции формируется URL для запроса к Steam Web API, который получает детали игры по ее AppID.
5. Выполняется GET-запрос к API и полученный ответ преобразуется в формат JSON.
6. Проверяется, содержит ли ответ информацию об игре. Если да, извлекается название игры и логируется его. Если нет, логируется сообщение о том, что игра не найдена.
7. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает None."""