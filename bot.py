from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from collections import defaultdict
from datetime import datetime
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Message Counter Storage
message_count = defaultdict(int)

# Function to Count Messages
def count_messages(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text

    # Count messages per user

    # Reply to confirm it’s working
    context.bot.send_message(chat_id, f"📊 You sent a message!")

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, count_messages))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
