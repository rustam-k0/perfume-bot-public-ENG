# perfume-bot/bot.py
# Main file: launches the Telegram bot, handles messages, and responds.

import os
import time
from dotenv import load_dotenv
import telebot

from database import get_connection, get_copies_by_original_id
from search import find_original
from formatter import format_response, welcome_text
from followup import schedule_followup_once

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram bot token
DB_PATH = os.getenv("DB_PATH", "data/perfumes.db")  # database path

# Token check
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env. Add the bot token.")

# Create TeleBot object
bot = telebot.TeleBot(BOT_TOKEN)

# Connect to the database
conn = get_connection(DB_PATH)

# Dictionaries to track user's last message and follow-up
last_user_ts = {}
followup_sent = {}

# /start or /help command — greeting
@bot.message_handler(commands=["start", "help"])
def start(msg):
    bot.reply_to(msg, welcome_text())

# Handle any text message
@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(msg):
    chat_id = msg.chat.id
    now = time.time()
    last_user_ts[chat_id] = now

    # Search for the original perfume
    result = find_original(conn, msg.text)

    if not result["ok"]:
        # Not found — ask for clarification
        bot.reply_to(msg, result["message"])
        return

    original = result["original"]
    # Get all available clones
    copies = get_copies_by_original_id(conn, original["id"])

    # Format a nice response and send
    bot.reply_to(msg, format_response(original, copies))

    # Schedule follow-up in 30 seconds (sent once)
    schedule_followup_once(bot, chat_id, now, last_user_ts, followup_sent)

# Start the bot
if __name__ == "__main__":
    print("Bot started — ready to receive messages.")
    try:
        # Start polling messages indefinitely
        bot.infinity_polling(timeout=60, long_polling_timeout=5)
    except Exception as e:
        print("Error while starting the bot:", e)
