import requests
from goldwise.config import telegram_config

def send_telegram_message(message: str):
    token, chat_id = telegram_config()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": chat_id, "text": message},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram delivery failed: {payload}")
    return payload
