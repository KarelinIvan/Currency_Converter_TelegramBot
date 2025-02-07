import os

from dotenv import load_dotenv

load_dotenv()

# Для работы с сервисом telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")