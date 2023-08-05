# Pip install pyTelegramBotAPI
"""_summary_
This contain the Linkedin automation of Text post using Telegram bot
"""

from telebot import TeleBot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from linkedin_automate_folder.linkedin_file import LinkedinAutomate
from linkedin_automate_folder.consts import POST_TYPE_TEXT, POST_TYPE_URL, GROUP_POST, MY_FEED, BOTH, BASE_LINKEDIN_URL_FOR_POST

TELEGRAM_TOKEN = os.environ.get("NEW_TELEGRAM_BOT_TOKEN") 
LINKEDIN_TOKEN = os.environ.get("LINKEDIN_ACCESS_KEY")
bot = TeleBot(TELEGRAM_TOKEN)

user_info = {}

def feed_type_selection():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("My Feed", callback_data="my_feed"),
        InlineKeyboardButton("Groups", callback_data="group"),
        InlineKeyboardButton("Both", callback_data="both")
    )
    return markup

def confirmation_selection():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="yes"),InlineKeyboardButton("No", callback_data="no"))
    return markup

# Idea for Description of Video
# Start with, this post is automated.....
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
/help and /start to get the help
/linkedin_post to post in linkedin
""")


@bot.message_handler(commands=['linkedin_post'])
def linkedin_post_handler(message):
    bot.send_message(message.chat.id, "Select which type of Post you want to make", reply_markup=feed_type_selection())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
    
def process_text_post(message):
    text = message.text
    user_info["description"] = text
    bot.send_message(message.chat.id, \
f"""
    Is the below description you want to post ??

<b>{text}</b>
"""\
,reply_markup=confirmation_selection(), parse_mode="html")

# @bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(lambda query: query.data in ["my_feed", "group", "both"])
def post_type_callback_handler(call):
    if call.data == "my_feed":
        user_info["feed_type"] = MY_FEED
    elif call.data == "group":
        user_info["feed_type"] = GROUP_POST
    elif call.data == "both":
        user_info["feed_type"] = BOTH
    else:
        bot.send_message(call.message, "Something went wrong")

    msg = bot.reply_to(call.message, 'Great, please write the text message you want to post')
    bot.register_next_step_handler(msg, process_text_post)
        # msg = bot.reply_to(yt_url_msg, 'Great, now please enter the description')
        # bot.register_next_step_handler(msg, process_text_post, "description")

@bot.callback_query_handler(lambda query: query.data in ["yes", "no"])
def confirmation_callback_handler(call):
    if call.data == "yes":
        description = user_info["description"]
        feed_type = user_info["feed_type"]
        post_media_category = POST_TYPE_TEXT
        msg = bot.reply_to(call.message, f'postinggg this msg......... {description}')

        post_respose = LinkedinAutomate(LINKEDIN_TOKEN, description, feed_type, post_media_category).main_func()
        print(post_respose)
        url_of_post = f"{BASE_LINKEDIN_URL_FOR_POST}{post_respose.headers.get('x-linkedin-id')}"
        bot.reply_to(msg, f'Posteddddd, this is the url - {url_of_post}')
    elif call.data == "no":
        msg = bot.reply_to(call.message, "Then what??")
        bot.register_next_step_handler(msg, process_text_post)



# Step 3: Start infinite polling
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
bot.infinity_polling()

