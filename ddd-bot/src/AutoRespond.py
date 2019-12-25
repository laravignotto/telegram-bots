from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import telegram
# import requests
from emoji import emojize
import os

class AutoRespond:
    dp = None
    
    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher

    def autoRespond(self, update, context):
        chat_id = update.message.chat_id
        prev_msg = update.message.text.lower()
        words = ["credo", "mi pare"]
        for w in words:
            if w in prev_msg:
                context.bot.send_message(chat_id=chat_id,
                                    text=emojize(w.capitalize(), use_aliases=True),
                                    parse_mode=telegram.ParseMode.MARKDOWN)

    def registerToDispatcher(self):
        self.dp.add_handler(MessageHandler(Filters.text, self.autoRespond))

