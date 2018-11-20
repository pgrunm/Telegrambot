#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import json
import logging
import random
import re
import sched
import time
from datetime import datetime, time, timedelta
from uuid import uuid4

import requests
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InlineQueryResultArticle, InputTextMessageContent,
                      ParseMode)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          InlineQueryHandler, MessageHandler, Updater)
from telegram.utils.helpers import escape_markdown

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

    # Packt source URL
    source_url_from_packt = 'https://www.packtpub.com/packt/offers/free-learning'

    # Requesting the web page
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    r = requests.get(source_url_from_packt, headers=headers)

    # Extracting the book title with some lovely regex.
    book_title = pattern.findall(str(r.text))
    str_to_return = 'The today\'s book is: {}. Find it at {}'.format(
        book_title[0], source_url_from_packt)
    return str_to_return


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


def number_to_unicode(number):
    '''
    Converting a digit into a unicode number smiley.
    See more at https://unicode.org/emoji/charts/full-emoji-list.html#keycap.
    '''
    unicode_numbers = {
        0: u'0️⃣',
        1: u'1️⃣',
        2: u'2️⃣',
        3: u'3️⃣',
        4: u'4️⃣',
        5: u'5️⃣',
        6: u'6️⃣',
        7: u'7️⃣',
        8: u'8️⃣',
        9: u'9️⃣',
    }
    number_for_return = u''

    # In case of a negative number:
    if number < 0:
        number *= -1

    while number != 0:
        number_for_return = unicode_numbers[number % 10] + number_for_return
        number = int(number / 10)

    return number_for_return


def timeleft(bot, update):
    arrival_time = datetime(2018, 12, 22, 18, 0)
    d = arrival_time - datetime.now()

    # Getting the hours
    hours = d.seconds / 3600
    minutes = d.seconds % 3600 / 60
    seconds = (minutes - int(minutes)) * 60

    msg = 'Bis zum 22. Dezember um 18 Uhr sind es noch: {} Tage, {} Stunden, {} Minuten und {} Sekunden.'.format(
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
