#Получение Steam User ID из ссылки профиля Steam

import logging
import os
import xml.etree.ElementTree as ET

import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция получения Steam User ID из ссылки профиля Steam
def get_user_id(profile_url, api_key):
    try:
        if not profile_url:
            logging.error("Пустая ссылка профиля Steam.")
            return None

        # Проверяем, является ли URL ссылкой на пользовательский или числовой профиль
        if "steamcommunity.com/id/" in profile_url:
            vanity_url = profile_url.split("steamcommunity.com/id/", 1)[1].split("/")[0]

            # Используем переданный API ключ или значение из переменных окружения
            api_key = api_key or os.getenv("STEAM_API_KEY")
            if not api_key:
                logging.info("Steam API ключ не задан, пробуем получить Steam ID по XML профиля.")
                return _resolve_vanity_via_xml(vanity_url, profile_url)

            url = (
                "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
                f"?key={api_key}&vanityurl={vanity_url}&url_type=1"
            )
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.error(
                    "Ошибка при обращении к Steam API для Vanity URL %s: код %s",
                    vanity_url,
                    response.status_code,
                )
                return None

            data = response.json()

            # Проверяем успешность ответа
            api_response = data.get("response", {})
            if api_response.get("success") == 1 and api_response.get("steamid"):
                steam_user_id = api_response["steamid"]

                # Проверяем соответствие с данными профиля, если возможно
                xml_steam_user_id = _resolve_vanity_via_xml(vanity_url, profile_url)
                if xml_steam_user_id and xml_steam_user_id != steam_user_id:
                    logging.info(
                        "Steam API вернул %s, но XML профиль содержит %s. Используем значение из XML.",
                        steam_user_id,
                        xml_steam_user_id,
                    )
                    return xml_steam_user_id

                logging.info(
                    "Получен Steam User ID: %s для профиля %s.",
                    steam_user_id,
                    profile_url,
                )
                return steam_user_id

            logging.error("Не удалось разрешить Vanity URL через Steam API: %s.", vanity_url)
            return _resolve_vanity_via_xml(vanity_url, profile_url)

        if "steamcommunity.com/profiles/" in profile_url:
            steam_user_id = profile_url.split("steamcommunity.com/profiles/", 1)[1].split("/")[0]
            logging.info(
                "Получен Steam User ID: %s для профиля %s.",
                steam_user_id,
                profile_url,
            )
            return steam_user_id

        logging.error("Неверный формат URL профиля: %s.", profile_url)
        return None
    except Exception as e:
        logging.error("Ошибка при получении Steam User ID из URL %s: %s", profile_url, e)
        return None
# Вспомогательная функция для получения SteamID через XML профиль
def _resolve_vanity_via_xml(vanity_url, profile_url):
    try:
        vanity_profile_xml = f"https://steamcommunity.com/id/{vanity_url}/?xml=1"
        response = requests.get(vanity_profile_xml, timeout=10)
        if response.status_code != 200:
            logging.error(
                "Не удалось получить XML профиль для Vanity URL %s: код %s",
                vanity_url,
                response.status_code,
            )
            return None

        xml_root = ET.fromstring(response.content)
        steam_id64_elem = xml_root.find("steamID64")
        if steam_id64_elem is not None and steam_id64_elem.text:
            steam_user_id = steam_id64_elem.text.strip()
            logging.info(
                "Получен Steam User ID через XML: %s для профиля %s.",
                steam_user_id,
                profile_url,
            )
            return steam_user_id

        logging.error("В XML профиля отсутствует steamID64 для Vanity URL: %s.", vanity_url)
        return None
    except Exception as xml_error:
        logging.error(
            "Ошибка при получении Steam User ID через XML для Vanity URL %s: %s",
            vanity_url,
            xml_error,
        )
        return None
  
  
    
"""
Как работает этот код:
1. Импортируются необходимые модули: logging для логирования и requests для выполнения HTTP-запросов.
2. Настраивается логирование на уровень INFO.
3. Определяется функция get_steam_user_id, которая принимает URL профиля Steam.
4. Внутри функции проверяется, является ли URL ссылкой на пользовательский (vanity) или числовой профиль.
5. Если это vanity URL, извлекается часть URL и выполняется запрос к Steam API для получения числового SteamID.
6. Если это числовой профиль, извлекается SteamID напрямую из URL.
7. Логируется полученный Steam User ID или ошибка, если что-то пошло не так.
8. В случае возникновения ошибки во время запроса или обработки данных, ошибка логируется, и функция возвращает None.
Возможности функции:
1. Обрабатывает оба типа URL профилей Steam: пользовательские и числовые. 
2. Использует Steam API для разрешения vanity URL в числовой SteamID.
"""