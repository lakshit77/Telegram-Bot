# Pip install pyTelegramBotAPI
# This code contain just 3 step guide to start the telegram bot

from telebot import TeleBot
import os

# Idea for Description of Video
# Start with, this post is automated.....

# Step 2: Add Bot Token
TELEGRAM_TOKEN = os.environ.get("NEW_TELEGRAM_BOT_TOKEN") 
bot = TeleBot(TELEGRAM_TOKEN)

# Step 2: Add the message handler
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    # bot.reply_to(message, "Hi! Use /set <seconds> to set a timer")
    bot.send_message(message.chat.id, "Hello there, from Linkedin bot")

# Step 3: Start infinite polling

bot.infinity_polling()

