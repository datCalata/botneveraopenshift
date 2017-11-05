# Copyright (C) 2016 Javier Ayres
#
# This file is part of python-telegram-bot-openshift.
#
# python-telegram-bot-openshift is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-telegram-bot-openshift is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-telegram-bot-openshift.  If not, see <http://www.gnu.org/licenses/>.

import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, Updater
import bot_telegram_callback

TOKEN = '460631781:AAEzUbO50_7B7zS3qj-WM89s9pi_9jXdRcU'


def example_handler(bot, update):
    # Remove this handler
    bot.send_message(
        update.message.chat_id,
        text='Hello from openshift'
    )

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
    dp.add_handler(MessageHandler([], example_handler))  # Remove this line
    start_handler = CommandHandler('start',bot_telegram_callback.start) #Callback
    comprar_handler = CommandHandler('comprar',bot_telegram_callback.comprar,pass_user_data=True)
    mete_dinero_handler = CommandHandler('metedinero',bot_telegram_callback.mete_dinero,pass_args=True)
    dinero_handler = CommandHandler('dinero',bot_telegram_callback.dinero)
    comprar_query_handler = CallbackQueryHandler(bot_telegram_callback.button,pass_user_data=True)
    ayuda_handler = CommandHandler('ayuda',bot_telegram_callback.ayuda)
    dispatcher.add_handler(comprar_query_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(comprar_handler)
    dispatcher.add_handler(mete_dinero_handler)
    dispatcher.add_handler(dinero_handler)
    dispatcher.add_handler(ayuda_handler)
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
