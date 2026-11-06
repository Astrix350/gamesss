import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")

try:
    ADMIN_ID = int(ADMIN_ID_STR)
except ValueError:
    raise ValueError("Переменная окружения ADMIN_ID должна быть числом!")