import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import os

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📘 Получить гайд")
    keyboard.add("💬 Поддержка")
    keyboard.add("🧭 Записаться на разбор")
    keyboard.add("📢 Telegram-канал")
    return keyboard

@dp.message_handler(commands=['start'])
async def start(mess
