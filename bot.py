from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from collections import defaultdict
from datetime import datetime
from transformers import pipeline
from apscheduler.schedulers.background import BackgroundScheduler
import os

# Get bot token from Render environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = "YOUR_GROUP_CHAT_ID"  # Replace with your Telegram group chat ID

# Message counter storage
message_count = defaultdict(int)
topic_count = defaultdict(int)

# Load AI topic detection model
topic_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Function to count messages and detect topics
def count_messages(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text

    # Count messages per user
    message_count[(chat_id, user_id, datetime.now().date())] += 1

    # Detect main topic
    candidate_topics = ["business", "sports", "technology", "politics", "entertainment", "health", "science"]
    result = topic_model(text, candidate_labels=candidate_topics)
    main_topic = result["labels"][0]  # Most relevant topic

    # Store topic count
    topic_count[(chat_id, main_topic)] += 1

    # Send topic detection result
    context.bot.send_message(chat_id, f"📌 Detected Topic: {main_topic}")

# Function to send daily report
def send_daily_report(context: CallbackContext):
    today = datetime.now().date()
    report = f"📊 Daily Report for {today}\n"

    # User message counts
    report += "\n🔹 **Messages per User:**\n"
    for (chat, user, date), count in message_count.items():
        if date == today:
            report += f"👤 User {user}: {count} messages\n"

    # Top topics discussed
    report += "\n📌 **Top Topics Discussed:**\n"
    for (chat, topic), count in topic_count.items():
        report += f"📢 {topic}: {count} mentions\n"

    # Send report to group
    context.bot.send_message(GROUP_CHAT_ID, report)

    # Reset counters after sending report
    message_count.clear()
    topic_count.clear()

# Main function to start the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, count_messages))

    # Schedule daily report at 23:59
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_report, 'cron', hour=23, minute=59, args=[updater.bot])
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
