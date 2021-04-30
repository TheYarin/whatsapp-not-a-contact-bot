import logging
import os
from time import sleep
from logging.handlers import RotatingFileHandler

from telegram import ChatAction, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from helpers import format_phone_number, trim_with_message_if_too_long
from settings import LOG_CHAT_ID, LOGS_FOLDER, TELEGRAM_BOT_TOKEN

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

def log_info_and_send_to_log_chat(message: str, context: CallbackContext) -> None:
    logger.info(message)
    context.bot.send_message(chat_id=LOG_CHAT_ID, text=message)


def handle_potential_number_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    formatted_phone_number = format_phone_number(update.message.text)
    
    log_info_and_send_to_log_chat(
f"""Received the following from {get_user_info(update)}:
{trim_with_message_if_too_long(update.message.text)}
Formatted to: {formatted_phone_number}""", context)
    
    if formatted_phone_number is None:
        update.message.reply_text("Bad format. Try something like +972-50-123-4567.")
    else:
        url = f'https://api.whatsapp.com/send/?phone={formatted_phone_number}'
        update.message.reply_text(url)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    log_info_and_send_to_log_chat(f"Started from {get_user_info(update)}", context)
    
    update.message.reply_text(
"""
Simply send me a phone number in almost any format, and I'll send you a WhatsApp link to it.
If you send me a local number (without a country code), I'll assume you mean Israel and use 972.
""")

def ping(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("pong")

def create_suspense(context: CallbackContext) -> None:
    context.bot.send_chat_action(context.job.context, action=ChatAction.TYPING)

def send_youre_welcome(context: CallbackContext) -> None:
    context.bot.send_message(context.job.context, text="Awww, you're welcome!")

def thanks(update: Update, context: CallbackContext) -> None:
    log_info_and_send_to_log_chat(f"{get_user_info(update)} says thank you!", context)
    
    chat_id = update.message.chat_id
    context.job_queue.run_once(create_suspense, when=2, context=chat_id, name=str(chat_id))
    context.job_queue.run_once(send_youre_welcome, when=3.4, context=chat_id, name=str(chat_id))
    


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("thanks", thanks))
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
