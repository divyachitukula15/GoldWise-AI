import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing {name} in .env")
    return value

def database_config() -> dict:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return {
            "conninfo": database_url,
            "sslmode": "require"
        }

    return {
        "host": get_required_env("DB_HOST"),
        "port": int(get_required_env("DB_PORT")),
        "dbname": get_required_env("DB_NAME"),
        "user": get_required_env("DB_USER"),
        "password": get_required_env("DB_PASSWORD"),
    }

def telegram_config() -> tuple[str, str]:
    return (
        get_required_env("TELEGRAM_BOT_TOKEN"),
        get_required_env("TELEGRAM_CHAT_ID"),
    )
