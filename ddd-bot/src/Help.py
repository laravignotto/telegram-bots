from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import requests
import re
from emoji import emojize
import json

# Stages
FIRST, LAST = range(2)
# Callback data
COMANDI, ESC, RESTART = range(3)

class Help:
    '''
    Handles help menu to give informations
    about the "studenti uniud" group and the bot
    '''

    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher
        self.text = json.load(open("src/help_texts.json"))

    #CALL
    def help(self, update, context):
        chat_id = update.message.chat_id
        keyboard = [
                    [InlineKeyboardButton("Comandi", callback_data=str(COMANDI))],
                    [InlineKeyboardButton("·Esci·", callback_data=str(ESC))],
                    ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["help_text"]
        update.message.reply_text(text,
                                reply_markup=reply_markup)
        return FIRST

    def start_over(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
                    [InlineKeyboardButton("Comandi", callback_data=str(COMANDI))],
                    [InlineKeyboardButton("·Esci·", callback_data=str(ESC))],
                    ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["help_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text,
            reply_markup=reply_markup
        )
        return FIRST

    def commands(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
            [InlineKeyboardButton("« Indietro", callback_data=str(RESTART)),
            InlineKeyboardButton("·Esci·", callback_data=str(ESC))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["commands_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=emojize(text, use_aliases=True),
            reply_markup=reply_markup,
            disable_web_page_preview = True
        )
        return LAST

    def done(self, update, context):
        query = update.callback_query
        bot = context.bot
        text = self.text["done_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text
        )
        return ConversationHandler.END

    def registerToDispatcher(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('help', self.help)],

            states={
                    FIRST: [CallbackQueryHandler(self.commands, pattern='^' + str(COMANDI) + '$'),
                            CallbackQueryHandler(self.done, pattern='^' + str(ESC) + '$')],
                    LAST: [CallbackQueryHandler(self.start_over, pattern='^' + str(RESTART) + '$'),
                            CallbackQueryHandler(self.done, pattern='^' + str(ESC) + '$')]
            },

            fallbacks=[CommandHandler('help', self.help)],
            persistent=True, name='help_persistence'
        )
        self.dp.add_handler(conv_handler)
