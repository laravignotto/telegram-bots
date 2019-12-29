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

        text = "Ciao, sono AsparagorgoBot! :smiley:\n\nScrivi /help per ricevere informazioni e consultare la lista dei comandi."
        context.bot.send_message(chat_id=chat_id, 
                    text=emojize(text, use_aliases=True),
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    )
        
        # Counts how many users start the bot
        # To restart the counting, change the number in num_of_users.txt to 0
        with open("num_of_users.txt", "r") as f:
            num = int(f.read())
            num += 1

        with open("num_of_users.txt", "w") as f:
            f.write(str(num))

    def registerToDispatcher(self):
        self.dp.add_handler(CommandHandler('start', self.start))
        