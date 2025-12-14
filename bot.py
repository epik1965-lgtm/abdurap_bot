import logging
import os
import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ===============================
#   НАСТРОЙКИ
# ===============================

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN is not set")

TIMEZONE = pytz.timezone("Europe/Moscow")
SEND_HOUR = 2
SEND_MINUTE = 0

USERS_FILE = "users.txt"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===============================
#   СООБЩЕНИЯ
# ===============================

MESSAGES = [
    # Сообщение 1
    """Тревога за диабет не берётся из ниоткуда.
Усталость, тянет на сладкое, вес растёт, в семье у кого-то уже диабет — и в голове картинка: «я следующая» 😶‍🌫️
Сдаёшь сахар — «вроде норма», а внутри легче не становится.

Это не про «накрутила себя».
Чаще всего тело правда даёт сигналы: сахар, желчь, ЖКТ, щитовидка, стресс, надпочечники — всё давно связано между собой, просто никто не собрал это в одну схему.""",

    # Сообщение 2
    """Диабет редко начинается по принципу «вчера всё было хорошо, сегодня — диагноз».

Сначала идёт длинный коридор:
– инсулинорезистентность,
– скачки сахара,
– лишний вес именно на животе,
– срывы на сладкое,
– сонливость после еды,
– хронический стресс, недосып, «нервы на пределе».

Это стадия, на которой ещё можно разворачивать ситуацию, если понимать, что смотреть и что менять.""",

    # Сообщение 3
    """В эту историю почти всегда включается не только сахар.

Желчь и ЖКТ: застой желчи = жиры хуже перевариваются, растёт воспаление, меняется чувствительность к инсулину.

Щитовидка: если она тормозит — падает метаболизм, холод, отёки, усталость.

Стресс и надпочечники: кортизол годами держит организм в тревоге.

То есть тревога про диабет — это связка:
инсулин + желчь + ЖКТ + щитовидка + стресс.""",

    # Сообщение 4
    """Типичные сигналы от желчи и ЖКТ:
– горечь во рту по утрам;
– тяжесть или боль справа под рёбрами;
– вздутие после жирной еды;
– нестабильный стул.

Параллельно:
– усталость,
– туман в голове,
– тревожность,
– плохой сон,
– зябкость и отёки.

Это не 10 болезней.
Это одна цепочка.""",

    # Сообщение 5
    """Мини-чек.

Ответь себе «да/нет»:

– тянет на сладкое;
– после еды клонит в сон;
– есть горечь во рту;
– тяжесть справа;
– вес растёт в животе;
– мерзнешь, отекаешь;
– нервы и плохой сон.

Если «да» больше 2–3 — это уже системный сбой, а не фантазии.""",

    # Сообщение 6
    """Внутри закрытого сообщества мы собираем это в схему.

Разбираем:
– где тревога обоснована,
– какие анализы нужны,
– как связаны сахар, желчь, ЖКТ, щитовидка, стресс,
– какие первые шаги реально облегчают состояние.

Без диет, без фанатизма, без запугивания.""",

    # Сообщение 7
    """Если ты живёшь с мыслью «я докачусь до диабета»
и параллельно мучают вздутие, усталость, тревога и срывы —

нет смысла дальше ходить по кругу.

Подписывайся на закрытое сообщество по кнопке ниже.
Внутри — разборы, чек-листы и понятный план действий."""
]

# ===============================
#   USERS STORAGE
# ===============================

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                uid, idx = line.strip().split("|")
                users[int(uid)] = int(idx)
    return users


def save_users(users):
    with open(USERS_FILE, "w") as f:
        for uid, idx in users.items():
            f.write(f"{uid}|{idx}\n")

# ===============================
#   START
# ===============================

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    users = load_users()
    uid = message.from_user.id

    if uid not in users:
        users[uid] = 1  # следующее сообщение — №2
        save_users(users)

    await message.answer(MESSAGES[0])

# ===============================
#   DAILY SENDER
# ===============================

async def daily_sender():
    while True:
        now = datetime.now(TIMEZONE)
        target = now.replace(hour=SEND_HOUR, minute=SEND_MINUTE, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)

        await asyncio.sleep((target - now).total_seconds())

        users = load_users()

        for uid, idx in list(users.items()):
            if idx < len(MESSAGES):
                try:
                    await bot.send_message(uid, MESSAGES[idx])
                    users[uid] += 1
                except Exception as e:
                    logging.warning(f"Failed to send to {uid}: {e}")

        save_users(users)

# ===============================
#   STARTUP
# ===============================

async def on_startup(dp):
    asyncio.create_task(daily_sender())

# ===============================
#   MAIN
# ===============================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)








