#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
import re
import sched
import time
from datetime import time

import certifi
import urllib3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

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


def parse_today_ebook():
    """Returns the current ebook from packtpub"""
    # Search for any big Header and return it
    pattern = re.compile(r'<h1>(.+)<\/h1><\/div>')

    # Avoiding https warnings by checking the tls certificate.
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    source_url_from_packt = 'https://www.packtpub.com/packt/offers/free-learning'

    # Requesting the web page
    r = http.request(
        'GET', source_url_from_packt)

    # Extracting the book title with some lovely regex.
    book_title = pattern.findall(str(r.data))
    return book_title[0]


def packt(bot, update):
    """Displays the title and the url to the latest free ebook of packtpub"""
    book_title = parse_today_ebook()

    update.message.reply_text(
        'The today\'s book is: {}. Find it at https://www.packtpub.com/packt/offers/free-learning'.format(book_title))


def packt_scheduled(bot, job):
    """Displays the title and the url to the latest free ebook of packtpub"""

    book_title = parse_today_ebook()
    bot.send_message(chat_id=349463555, text='The today\'s book is: {}. Find it at https://www.packtpub.com/packt/offers/free-learning'.format(
        book_title))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("614151885:AAHqxtafQx-5aYP8U1zRB9oEgXTzZ2Awx1M")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('packt', packt))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_error_handler(error)

    # Adding a scheduled message at 3 o'clock in the morning to notify about the current latest book
    j = updater.job_queue
    j.run_daily(packt_scheduled, time(3, 0))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
