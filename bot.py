import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ---- НАСТРОЙКИ ----
TOKEN = os.getenv("TOKEN")

# Твой юзернейм для поддержки
SUPPORT_USERNAME = "@Alexander_Epik"

# Ссылки на Google Forms
FORM_1_URL = "https://forms.gle/xEVdkxzgUQa3cBAw6"   # карта тревожности
FORM_2_URL = "https://forms.gle/x8hXPySScixkKZtd8"   # карта усталости
DIABET_WORDS = ["диабет", "diabet", "diabetes"]

@dp.message_handler(lambda m: any(w.lower() in m.text.lower() for w in DIABET_WORDS))
async def send_diabet_guide(message: types.Message):
    await message.answer("Отправляю вам гайд по самому раннему сигналу диабета 💡")
    await message.answer_document(open("guide_diabet.pdf", "rb"))

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

    btn_test_1 = "📊 Пройти тест карты вашей тревожности"
    btn_test_2 = "📊 Пройти тест карты вашей усталости"

    keyboard.add(btn_guide)
    keyboard.add(btn_support)
    keyboard.add(btn_analysis)
    keyboard.add(btn_channel)
    keyboard.add(btn_test_1, btn_test_2)

    return keyboard


# ---- /start ----
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.full_name}!\n\n"
        f"Я бот Абдурапа. Выбери, что тебе нужно сейчас:",
        reply_markup=main_menu()
    )


# ---- ОБРАБОТКА КНОПОК ----
@dp.message_handler()
async def buttons(message: types.Message):
    text = message.text

    if text == "📘 Получить гайд":
        await message.answer("Секунду… загружаю файл…")

        file_path = "13_lifehacks.pdf"
        if os.path.exists(file_path):
            await message.answer_document(open(file_path, "rb"))
        else:
            await message.answer("❗ Файл не найден на сервере!")

    elif text == "💬 Поддержка":
        await message.answer(
            f"Если нужен контакт с командой или вопросы по работе с Абдурапом — "
            f"пиши сюда: {SUPPORT_USERNAME}"
        )

    elif text == "🧪 Записаться на разбор":
        await message.answer(
            "Чтобы записаться на разбор, напиши в личку: "
            f"{SUPPORT_USERNAME} и коротко опиши свою ситуацию.\n\n"
            "Команда вернётся к тебе с форматом и временем."
        )

    elif text == "📢 Telegram-канал":
        await message.answer(
            "Вот ссылка на канал с рекомендациями:\n"
            "https://t.me/your_channel"
        )

    elif text == "📊 Пройти тест карты вашей тревожности":
        await message.answer(
            "🧠 Тест «Карта вашей тревожности».\n\n"
            "Заполни форму — Абдурап увидит, как именно проявляется тревожность "
            "в твоей жизни, и сможет точнее подобрать рекомендации:\n"
            f"{FORM_1_URL}"
        )

    elif text == "📊 Пройти тест карты вашей усталости":
        await message.answer(
            "😴 Тест «Карта вашей усталости».\n\n"
            "Ответь на вопросы — это поможет понять уровень истощения, "
            "нагрузку и то, где именно ты «сливаешь» энергию:\n"
            f"{FORM_2_URL}"
        )

    else:
        await message.answer(
            "Не понял команду 🤔\n"
            "Выбери действие через меню ниже."
        )


# ---- ЗАПУСК ----
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



