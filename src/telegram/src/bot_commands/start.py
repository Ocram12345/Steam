#Обработка команды /start
from aiogram import types
from aiogram.filters import Command
from aiogram import Router
# Создание роутера и регистрация обработчика
router = Router()
# Обработчик команды /start
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я SteamCFM бот. Чем могу помочь?")

    
