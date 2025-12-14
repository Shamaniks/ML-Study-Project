import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests


def answer_to_user(update: Update, response):
    update.message.reply_text("There would be our response")


#answer_to_user(update, "")
