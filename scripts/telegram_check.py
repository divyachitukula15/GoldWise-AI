import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")

response = requests.get(
    f"https://api.telegram.org/bot{token}/getUpdates",
    timeout=20,
)
response.raise_for_status()
updates = response.json().get("result", [])

if updates:
    print("Chat ID:", updates[-1]["message"]["chat"]["id"])
else:
    print("Send /start to your Telegram bot, then run this script again.")
