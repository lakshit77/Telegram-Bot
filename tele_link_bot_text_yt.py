# This contain the Linkedin automation of Text post and URL post using Telegram bot

from telebot import TeleBot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from linkedin_automate_folder.linkedin_file import LinkedinAutomate
from linkedin_automate_folder.consts import POST_TYPE_TEXT, POST_TYPE_URL, GROUP_POST, MY_FEED, BOTH, BASE_LINKEDIN_URL_FOR_POST


user_info = {}

def post_type_selection():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Text", callback_data="text"),InlineKeyboardButton("Youtube", callback_data="yt_post"))
    return markup

def confirmation_selection():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="yes"),InlineKeyboardButton("No", callback_data="no"))
    return markup

# Idea for Description of Video
# Start with, this post is automated.....

# Step 2: Add Bot Token
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") 
LINKEDIN_TOKEN = os.environ.get("LINKEDIN_ACCESS_KEY")
bot = TeleBot(TELEGRAM_TOKEN)

# Step 2: Add the message handler
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
/help and /start to get the help
/linkedin_post to post in linkedin
""")


@bot.message_handler(commands=['linkedin_post'])
def linkedin_post_handler(message):
    bot.send_message(message.chat.id, "Select which type of Post you want to make", reply_markup=post_type_selection())

@bot.message_handler(func=lambda message: True)
def callback_postType_handler(message):
    bot.send_message(message, f"Answr is {message}")



def process_url_post(message):
    text = message.text
    user_info["yt_url"] = text
    msg = bot.reply_to(message, 'Great, now please enter the description')
    bot.register_next_step_handler(msg, process_text_post)
    # if key_type == "yt_url":
    #     return message
#     bot.send_message(message.chat.id, \
# f"""This is {key_type} you want to post
# {text}"""\
# ,reply_markup=confirmation_selection())
    
def process_text_post(message):
    text = message.text
    user_info["description"] = text
    bot.send_message(message.chat.id, \
f"""This is description you want to post
{text}"""\
,reply_markup=confirmation_selection())

# @bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(lambda query: query.data in ["text", "yt_post"])
def post_type_callback_handler(call):
    if call.data == "text":
        user_info["post_type"] = POST_TYPE_TEXT
        msg = bot.reply_to(call.message, 'Great, please write the text message you want to post')
        bot.register_next_step_handler(msg, process_text_post)
    elif call.data == "yt_post":
        user_info["post_type"] = POST_TYPE_URL
        msg = bot.reply_to(call.message, 'Great, please paste the Youtube URL you want to share')
        bot.register_next_step_handler(msg, process_url_post)
        # msg = bot.reply_to(yt_url_msg, 'Great, now please enter the description')
        # bot.register_next_step_handler(msg, process_text_post, "description")

@bot.callback_query_handler(lambda query: query.data in ["yes", "no"])
def confirmation_callback_handler(call):
    if call.data == "yes":
        description = user_info["description"]
        yt_url = user_info.get("yt_url")
        feed_type = MY_FEED
        post_media_category = user_info["post_type"]
        msg = bot.reply_to(call.message, f'postinggg this msg......... {description}')

        post_respose = LinkedinAutomate(LINKEDIN_TOKEN, description, feed_type, post_media_category, yt_url).main_func()
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

