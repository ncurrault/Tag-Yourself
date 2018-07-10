# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import telegram
from telegram.ext import Updater, CommandHandler, Filters
import logging
import os
import geometry

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

def get_graph_name(bot, update, args, validate_existence=True):
    if args is None or len(args) == 0:
        return None
    elif validate_existence and args[0] not in plots.keys():
        return None
    else:
        return args[0]

def newgraph_handler(bot, update, args=None):
    name = get_graph_name(bot, update, args, validate_existence=False)

    if name is None:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Error: syntax is /newgraph [NAME]")
    else:
        plots[name] = geometry.Plot(name)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Success! Created new '{}' plot".format(name))

def addaxis_handler(bot, update, args=None):
    if args and len(args) >= 2:
        name = get_graph_name(bot, update, args)

        if name is None:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Error: graph '{}' was not found!".format(name))
        else:
            label = " ".join(args[1:])

            plots[name].add_axis(label)
            bot.send_message(chat_id=update.message.chat_id,
                             text="Successfully added axis!")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Error: syntax is /addaxis [GRAPH NAME] [AXIS LABEL]")

def listaxes_handler(bot, update, args=None):
    name = get_graph_name(bot, update, args)
    if name is None:
        if args:
            bot.send_message(chat_id=update.message.chat_id,
                text="Error: graph '{}' was not found!".format(args[0]))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                text="Error: syntax is /listaxes [GRAPH NAME]")
    else:
        bot.send_message(chat_id=update.message.chat_id,
            text="Current axes: " + ", ".join(plots[name].get_axes()) )

def display_handler(bot, update, args=None):
    name = get_graph_name(bot, update, args)
    if name is None:
        if args:
            bot.send_message(chat_id=update.message.chat_id,
                text="Error: graph '{}' was not found!".format(args[0]))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                text="Error: syntax is /lookatthisgraph [GRAPH NAME]")
    else:
        image = plots[name].generate_image()
        # TODO spooky image-sending things
        bot.send_message(chat_id=update.message.chat_id,
            text=image)

def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#   /tag name coords  [point label]
def tag_handler(bot, update, args=None):
    if args and len(args) >= 2:
        name = get_graph_name(bot, update, args)

        if name is None:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Error: graph '{}' was not found!".format(args[0]))
        else:
            plot = plots[name]

            coords_and_label = " ".join(args[1:]).replace("(","").replace(")","").replace(","," ")
            items = coords_and_label.split()
            if len(items) < plot.dim:
                bot.send_message(chat_id=update.message.chat_id,
                text="Error: insufficent coordinates for {}-dimensional graph".format(plot.dim))
                return
            elif len(items) == plot.dim:
                coords_strs = items
                label = update.message.from_user.first_name[0] + update.message.from_user.last_name[0]
                    # user initials
            else: # len(items) > plot.dim
                coords_strs = items[:plot.dim]
                label = " ".join(items[plot.dim:])

            if not all( [is_numeric(s) for s in coords_strs]):
                bot.send_message(chat_id=update.message.chat_id,
                    text="Error: all coordinates must be numbers")
            else:
                point = geometry.Point(label, plot.dim)
                point.set_data_arr([ float(s) for s in coords_strs ])
                plot.add_point(point)

                bot.send_message(chat_id=update.message.chat_id,
                    text="Successfully added point {}".format(point) )

    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Error: syntax is /tag [GRAPH NAME] [COORDINATE] [COORDINATE] ... [optional label]")


dispatcher.add_handler(CommandHandler('newgraph', newgraph_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('addaxis', addaxis_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('listaxes', listaxes_handler, pass_args=True))
dispatcher.add_handler(CommandHandler(['lookatthisgraph', 'latg'], display_handler, pass_args=True))
dispatcher.add_handler(CommandHandler('tag', tag_handler, pass_args=True))


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
