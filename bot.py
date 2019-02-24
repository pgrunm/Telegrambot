#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import json
import logging
import random
import sched
import time
from datetime import datetime, time, timedelta
from uuid import uuid4

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InlineQueryResultArticle, InputTextMessageContent,
                      ParseMode)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          InlineQueryHandler, MessageHandler, Updater)
from telegram.utils.helpers import escape_markdown

from bot_functions import number_to_unicode, parse_today_ebook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("Welcome!")


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text('''Available commands:
    /start
    /packt
    /help''')


def packt(bot, update):
    """Displays the title and the url to the latest free ebook of packtpub"""
    message = parse_today_ebook()
    # Send the reply message
    update.message.reply_text(message)


def packt_scheduled(bot, job):
    """Displays the title and the url to the latest free ebook of packtpub"""

    message = parse_today_ebook()
    # Send the reply message
    bot.send_message(chat_id=-112906790, text=message)


def joke(bot, update):
    """Handle the inline query when mentioning the bot and return a joke."""

    # Load the jokes from the locally downloaded file
    file = open('data.json')
    data = json.load(file)['jokes']

    # Choose a random joke and format it accordingly
    joke = random.choice(list(data))
    reply = 'Titel: {}\n{}'.format(joke['Titel'], joke['Text'])
    query = update.inline_query.query
    if not query:
        return
    results = list()
    # Prepare the result and send it.
    results.append(
        InlineQueryResultArticle(
            id=query,
            title=joke['Titel'],
            input_message_content=(InputTextMessageContent(reply))
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def timeleft(bot, update):
    arrival_time = datetime(2019, 1, 16, 12, 0)
    d = arrival_time - datetime.now()

    # Getting the hours
    hours = d.seconds / 3600
    minutes = d.seconds % 3600 / 60
    seconds = (minutes - int(minutes)) * 60

    msg = 'Bis zum 16. Januar um 12 Uhr sind es noch: {} Tage, {} Stunden, {} Minuten und {} Sekunden.'.format(
        number_to_unicode(d.days), number_to_unicode(int(hours)), number_to_unicode(int(minutes)), number_to_unicode(int(seconds)))
    update.message.reply_text(msg)


def main():
    # Reading the API token from the bot.ini file
    config = configparser.ConfigParser()
    config.read('bot.ini')

    # Create the Updater and pass it your bot's token.
    updater = Updater(config['API']['Token'])

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('packt', packt))

    # Adding the Timeleft function.
    updater.dispatcher.add_handler(CommandHandler('time', timeleft))

    # Adding the inline ability for jokes
    updater.dispatcher.add_handler(InlineQueryHandler(joke))

    # Adding the reply for unknown messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.dispatcher.add_error_handler(error)

    # Adding a scheduled message at 4 o'clock to notify about the latest book
    j = updater.job_queue
    j.run_daily(packt_scheduled, time(4, 0))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
