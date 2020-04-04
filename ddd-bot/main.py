# telegram apis
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, PicklePersistence, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import requests

#standard apis
import os
import json, sys
import re
from emoji import emojize
from PIL import Image
from PIL import ImageDraw, ImageFont
import logging
import textwrap
import random 

# bot apis
from src.Start import Start
from src.Help import Help
from src.Dancanize import Dancanize
from src.AutoRespond import AutoRespond
from src.DancanText import DancanText


class Bot:
    def __init__(self):
        self.config = json.load(open("resources/config.json"))
        token = self.config["token"]
        self.main(token)

    def main(self, tk):
        '''
        Executes bot code and handles bot polling/lifecycle
        '''
        # persistence
        my_persistence = PicklePersistence(filename='persistence')
        updater = Updater(tk, persistence=my_persistence, use_context=True)
        # for security purposes, everytime main will be called, the token
        # attribute will be erased from object memory
        del tk

        dp = updater.dispatcher
        jobQueue = updater.job_queue

        # commands
        start = Start(self, dp)
        start.registerToDispatcher()

        help = Help(self, dp)
        help.registerToDispatcher()

        dancanize = Dancanize(self, dp)
        dancanize.registerToDispatcher()

        autorespond = AutoRespond(self, dp)
        autorespond.registerToDispatcher()

        dancantext = DancanText(self, dp)
        dancantext.registerToDispatcher()

        self.enableLogging()

        # start the bot
        updater.start_polling()
        updater.idle()
    
    def enableLogging(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    def isBot(self):
        '''
        Uniquely identifies the main bot class.
        Used mainly in assertions.
        '''
        return True


b = Bot()