import os
from dotenv import load_dotenv

load_dotenv()


def get_env_var_yell_if_missing(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise Exception('Missing environment variable: ' + key)

    return value


TELEGRAM_BOT_TOKEN = get_env_var_yell_if_missing("TELEGRAM_BOT_TOKEN")
LOGS_FOLDER = get_env_var_yell_if_missing("LOGS_FOLDER")