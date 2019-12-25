from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import telegram
import requests
import re
from emoji import emojize

class Start:
    '''
    Handles /start command
    '''
    dp = None
    
    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher
    
    def start(self, update, context):
        chat_id = update.message.chat_id

        text = "Ciao, Sono dddBot! :four_leaf_clover:\n\nScrivi /help per ricevere informazioni e consultare la lista dei comandi."
        context.bot.send_message(chat_id=chat_id, 
                    text=emojize(text, use_aliases=True),
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    )

    def registerToDispatcher(self):
        self.dp.add_handler(CommandHandler('start', self.start))
        