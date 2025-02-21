from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = "8181011652:AAHv408VJyQkw1tXnbxpM3r5K8ZljItEgko"

def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    update.message.reply_text(f"Your Chat ID: {chat_id}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("getid", get_chat_id))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
