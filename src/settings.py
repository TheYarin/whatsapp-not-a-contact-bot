import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var_yell_if_missing(key: str) -> str:
    if (value := os.getenv(key)) is None:
        raise Exception('Missing environment variable: ' + key)

    return value


TELEGRAM_BOT_TOKEN = get_env_var_yell_if_missing("TELEGRAM_BOT_TOKEN")
LOGS_FOLDER = './logs'
LOG_CHAT_ID = int(get_env_var_yell_if_missing("LOG_CHAT_ID"))
BELOVED_USER_ID = int(get_env_var_yell_if_missing("BELOVED_USER_ID"))
