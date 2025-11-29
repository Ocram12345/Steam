# Обработка команды /help
from aiogram import Router, types
from aiogram.filters import Command
# Создание роутера и регистрация обработчика
router = Router()
# Обработчик команды /help
@router.message(Command(commands=['help']))
async def send_help(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Запустить бота и получить приветственное сообщение.\n"
        "/help - Показать это справочное сообщение.\n"
        "/steam_profile <URL или имя пользователя> - Получить и сохранить SteamID пользователя.\n"
        "/view_user_profile - Просмотреть сохранённый профиль Steam.\n"
        # Добавьте здесь другие команды по мере необходимости
    )
    await message.answer(help_text)