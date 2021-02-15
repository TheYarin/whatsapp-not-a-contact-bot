import os

import logging
from logging.handlers import RotatingFileHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from settings import TELEGRAM_BOT_TOKEN, LOGS_FOLDER
from phone_number_formatting import format_phone_number

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(os.path.join(LOGS_FOLDER, "log.txt"), maxBytes=100 * 1024**2, backupCount=2), # 200MB
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def get_user_info(update: Update) -> str:
    user = update.message.from_user
    user_id = user.id
    full_name = user.full_name
    username = user.username

    return f'user_id: {user_id}, username: "{username}", full name: "{full_name}"'

def handle_potential_number_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    formatted_phone_number = format_phone_number(update.message.text)
    
    if formatted_phone_number is None:
        logger.info(f"Received bad format from {get_user_info(update)}")
        update.message.reply_text("Bad format. Try something like +972-50-123-4567.")
    else:
        logger.info(f"Received {formatted_phone_number} from {get_user_info(update)}")
        url = f'https://api.whatsapp.com/send/?phone={formatted_phone_number}'
        update.message.reply_text(url)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger.info(f"Started from {get_user_info(update)}")
    
    update.message.reply_text(
"""
Simply send me a phone number in almost any format, and I'll send you a WhatsApp link to it.
If you send me a local number (without a country code), I'll assume you mean Israel and use 972.
""")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_potential_number_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()