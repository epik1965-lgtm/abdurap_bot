import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ---- TOKEN ----
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# ---- КЛАВИАТУРА ----
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_guide = "📘 Получить гайд"
    btn_support = "💬 Поддержка"
    btn_analysis = "🧪 Записаться на разбор"
    btn_channel = "📢 Telegram-канал"

    keyboard.add(btn_guide)
    keyboard.add(btn_support)
    keyboard.add(btn_analysis)
    keyboard.add(btn_channel)

    return keyboard


# ---- /start ----
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.full_name}!\n\n"
        f"Я бот Абдурапа. Выберите действие ниже:",
        reply_markup=main_menu()
    )


# ---- ОБРАБОТКА КНОПОК ----
@dp.message_handler()
async def buttons(message: types.Message):
    text = message.text

    if text == "📘 Получить гайд":
        await message.answer("Секунду… Загружаю файл…")

        file_path = "13_lifehacks.pdf"
        if os.path.exists(file_path):
            await message.answer_document(open(file_path, "rb"))
        else:
            await message.answer("❗ Файл не найден на сервере!")

    elif text == "💬 Поддержка":
        await message.answer("Пиши сюда: @your_support")

    elif text == "🧪 Записаться на разбор":
        await message.answer("Записываю тебя на разбор! Ожидай ответа от команды.")

    elif text == "📢 Telegram-канал":
        await message.answer("Вот ссылка на канал: https://t.me/your_channel")

    else:
        await message.answer(
            "Не понял команду 🤔\n"
            "Выбери действие через меню."
        )


# ---- ЗАПУСК ----
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

