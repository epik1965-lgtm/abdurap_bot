import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Получаем токен из Railway переменной TOKEN
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📘 Получить гайд")
    keyboard.add("💬 Поддержка")
    keyboard.add("📝 Записаться на разбор")
    keyboard.add("📢 Telegram-канал")
    return keyboard


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = (
        "Привет, я Абдурап Мурзаев.\n\n"
        "Если ты здесь, значит хочешь разобраться со здоровьем: вернуть энергию,\n"
        "уменьшить усталость, стресс или наладить цикл.\n\n"
        "Внутри ты получишь:\n"
        "• Гайд по режиму\n"
        "• Разбор твоего состояния\n"
        "• Доступ к Telegram-каналу\n\n"
        "Напиши, что тебе важно сейчас."
    )
    await message.answer(text, reply_markup=main_menu())


@dp.message_handler(lambda msg: msg.text == "📘 Получить гайд")
async def send_guide(message: types.Message):
    await message.answer("Отправляю тебе гайд…")
    await message.answer_document(open("13_lifehacks.pdf", "rb"))


@dp.message_handler(lambda msg: msg.text == "💬 Поддержка")
async def support(message: types.Message):
    await message.answer("Напиши сюда свой вопрос, и мы тебе поможем.")


@dp.message_handler(lambda msg: msg.text == "📝 Записаться на разбор")
async def sign_up(message: types.Message):
    await message.answer("Чтобы записаться на разбор, напиши: «Хочу разбор».")


@dp.message_handler(lambda msg: msg.text == "📢 Telegram-канал")
async def send_channel(message: types.Message):
    await message.answer("Наш канал: https://t.me/—тут_ссылка—")


if name == "__main__":
    executor.start_polling(dp, skip_updates=True)
