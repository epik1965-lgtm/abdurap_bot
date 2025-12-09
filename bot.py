import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- TOKEN ---
TOKEN = os.getenv("TOKEN")   # Railway environment variable

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)

# --- BOT & DISPATCHER ---
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# ------------------------------
#  КНОПКИ
# ------------------------------
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_guide = "📘 Получить гайд"
    btn_support = "🆘 Поддержка"
    btn_test1 = "🧠 Пройти тест: карта тревожности"
    btn_test2 = "💤 Пройти тест: карта усталости"
    btn_channel = "📨 Telegram-канал"

    keyboard.add(btn_guide)
    keyboard.add(btn_test1)
    keyboard.add(btn_test2)
    keyboard.add(btn_support)
    keyboard.add(btn_channel)

    return keyboard
# ------------------------------
#   БАЗА ДАННЫХ
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Таблица пользователей
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            first_name  TEXT,
            last_name   TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Таблица действий
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS actions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            action      TEXT,
            meta        TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def upsert_user(message: types.Message):
    user = message.from_user

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username    = excluded.username,
            first_name  = excluded.first_name,
            last_name   = excluded.last_name,
            last_seen_at = CURRENT_TIMESTAMP
        """,
        (user.id, user.username, user.first_name, user.last_name),
    )

    conn.commit()
    conn.close()


def log_action(message: types.Message, action: str, meta: str | None = None):
    user_id = message.from_user.id

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO actions (user_id, action, meta)
        VALUES (?, ?, ?)
        """,
        (user_id, action, meta),
    )

    conn.commit()
    conn.close()


# ------------------------------
#  КНОПКИ
# ------------------------------
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_guide = "📘 Получить гайд"
    btn_support = "🆘 Поддержка"
    btn_test1 = "🧠 Пройти тест: карта тревожности"
    btn_test2 = "💤 Пройти тест: карта усталости"
    btn_channel = "📨 Telegram-канал"

    keyboard.add(btn_guide)
    keyboard.add(btn_test1)
    keyboard.add(btn_test2)
    keyboard.add(btn_support)
    keyboard.add(btn_channel)

    return keyboard

# ------------------------------
#   START COMMAND
# ------------------------------
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Добро пожаловать! 👋\n\nВыберите действие:",
        reply_markup=main_menu()
    )


# ------------------------------
#   ХЕНДЛЕРЫ НАЖАТИЙ КНОПОК
# ------------------------------

@dp.message_handler(lambda m: m.text == "📘 Получить гайд")
async def send_guide(message: types.Message):
    await message.answer_document(open("guide.pdf", "rb"))


@dp.message_handler(lambda m: m.text == "🧠 Пройти тест: карта тревожности")
async def anxiety_test(message: types.Message):
    await message.answer(
        "🧠 Тест на карту вашей тревожности:\n"
        "https://forms.gle/xEVdkxzgUQa3cBAw6"
    )


@dp.message_handler(lambda m: m.text == "💤 Пройти тест: карта усталости")
async def fatigue_test(message: types.Message):
    await message.answer(
        "💤 Тест на карту вашей усталости:\n"
        "https://forms.gle/x8hXPySScixkKZtd8"
    )


@dp.message_handler(lambda m: m.text == "🆘 Поддержка")
async def support(message: types.Message):
    await message.answer(
        "Если вам нужна помощь — пишите сюда:\n@Alexander_Epik"
    )


@dp.message_handler(lambda m: m.text == "📨 Telegram-канал")
async def channel(message: types.Message):
    await message.answer("Наш канал: https://t.me/+ZNYZ9n3nJwoyMzIy")


# ------------------------------
#   АВТО-ОТПРАВКА ГАЙДА ПО СЛОВУ «ДИАБЕТ»
# ------------------------------
DIABET_WORDS = ["диабет", "diabet", "diabetes"]


@dp.message_handler(lambda m: m.text and any(w in m.text.lower() for w in DIABET_WORDS))
async def send_diabet_auto(message: types.Message):
    await message.answer("Отправляю вам гайд по ранним сигналам диабета 💡")
    await message.answer_document(open("guide_diabet.pdf", "rb"))

BILE_WORDS = ["желчь","Желчь","ЖЕЛЧЬ"]

@dp.message_handler(lambda m: m.text and any(w in m.text.lower() for w in BILE_WORDS))
async def send_bile_auto(message: types.Message):
    await message.answer("Отправляю вам гайд по желчи.")
    await message.answer_document(open("liver_guide.pdf", "rb"))

# ------------------------------
#   MAIN LOOP
# ------------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



