# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler, Filters
import logging
import os
import matplotlib.pyplot as plt

with open("ignore/API_key.txt", "r") as f:
    API_KEY = f.read().rstrip()

PICKLE_STORAGE_DIRECTORY = "ignore"

updater = Updater(token=API_KEY)
dispatcher = updater.dispatcher

plots = {}

# restore any saved plots
for filename in os.listdir(PICKLE_STORAGE_DIRECTORY):
    if filename.endswith(".p"):
        plot_name = filename[:-2] # remove .p

        with open(os.path.join(PICKLE_STORAGE_DIRECTORY, filename), "r") as f:
            plots[plot_name] = pickle.load(f)

# TODO: actual handlers for
#   /newgraph name
#   /addaxis name label
#   /listaxes name
#   /lookatthisgraph name
#   /tag name coords  [point label]

# Credit: https://github.com/CaKEandLies/Telegram_Cthulhu/blob/master/cthulhu_game_bot.py#L63
def feedback_handler(bot, update, args=None):
    """
    Store feedback from users in a text file.
    """
    if args and len(args) > 0:
        feedback = open("ignore/feedback.txt", "a")
        feedback.write("\n")
        feedback.write(update.message.from_user.first_name)
        feedback.write("\n")
        # Records User ID so that if feature is implemented, can message them
        # about it.
        feedback.write(str(update.message.from_user.id))
        feedback.write("\n")
        feedback.write(" ".join(args))
        feedback.write("\n")
        feedback.close()
        bot.send_message(chat_id=update.message.chat_id,
                         text="Thanks for the feedback!")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Format: /feedback [feedback]")
dispatcher.add_handler(CommandHandler('feedback', feedback_handler, pass_args=True))

def start_handler(bot, update):
    with open("start.md", "r") as f:
        bot.send_message(chat_id=update.message.chat_id, text=f.read()[:-1],
            parse_mode=telegram.ParseMode.MARKDOWN) # remove trailing \n
def help_handler(bot, update):
    with open("help.md", "r") as f:
        bot.send_message(chat_id=update.message.chat_id, text=f.read()[:-1],
            parse_mode=telegram.ParseMode.MARKDOWN) # remove trailing \n
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO) # not sure exactly how this works

updater.start_polling()
updater.idle()
