import telegram
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from core.tasks import *
from decouple import config

token = config('TELEGRAM_BOT_TOKEN')

bot = telegram.Bot(token=token)

updates = bot.get_updates()

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, eu sou o OncoBot :D Fale comigo!")
    mailtest()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

