from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import requests
import re
from emoji import emojize
import json

# Stages
FIRST, LAST, STATE1 = range(3)
# Callback data
PROGRAM, MENU, WHERE, CONTACTS, MSG, ESC, BACK, RESTART = range(8)

class Info():
    '''
    Handles info menu that gives informations
    about the festival
    '''

    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher
        self.text = json.load(open("src/info_texts.json"))

    #CALL
    def info(self, update, context):
        chat_id = update.message.chat_id
        
        keyboard = [
                    [
                        InlineKeyboardButton("Programma", callback_data=str(PROGRAM)),
                        InlineKeyboardButton("Menù", callback_data=str(MENU))],
                    [
                        InlineKeyboardButton("Dove siamo", callback_data=str(WHERE)),
                        InlineKeyboardButton("Contatti", callback_data=str(CONTACTS))
                    ],
                    [
                        InlineKeyboardButton("·Esci·", callback_data=str(ESC))
                    ]
                ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["info_text"]
        update.message.reply_text(text,
                                reply_markup=reply_markup)
        # Tell CosversationHandler that we're in State `FIRST` now
        return FIRST

    def start_over(self, update, context):
        """Prompt same text & keyboard as `start` does but not as new message"""
        # Get CallbackQuery from Update
        query = update.callback_query
        # Get Bot from CallbackContext
        bot = context.bot
        keyboard = [
                    [
                        InlineKeyboardButton("Programma", callback_data=str(PROGRAM)),
                        InlineKeyboardButton("Menù", callback_data=str(MENU))],
                    [
                        InlineKeyboardButton("Dove siamo", callback_data=str(WHERE)),
                        InlineKeyboardButton("Contatti", callback_data=str(CONTACTS))
                    ],
                    [
                        InlineKeyboardButton("·Esci·", callback_data=str(ESC))
                    ]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Instead of sending a new message, edit the message that
        # originated the CallbackQuery. This gives the feeling of an
        # interactive menu.
        text = self.text["info_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text,
            reply_markup=reply_markup
        )
        return FIRST

    def programma(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
                    [
                        InlineKeyboardButton("« Indietro", callback_data=str(RESTART)),
                        InlineKeyboardButton("·Esci·", callback_data=str(ESC))
                    ]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # i put an empty character in the text link
        text = self.text["programma_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=text,
            reply_markup=reply_markup
        )
        return LAST

    def menu(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
            [InlineKeyboardButton(emojize(":meat_on_bone: Foto dei Piatti", use_aliases=True), url="http://www.asparagorgo.info/il-menu/")],
            [InlineKeyboardButton("« Indietro", callback_data=str(RESTART)),
            InlineKeyboardButton("·Esci·", callback_data=str(ESC))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["menu_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=emojize(text, use_aliases=True),
            reply_markup=reply_markup,
            disable_web_page_preview = True
        )
        return LAST

    def doveSiamo(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
            [InlineKeyboardButton(emojize(":round_pushpin: Google Maps", use_aliases=True), url="https://goo.gl/maps/dct8Td6YVtH6CHsG8")],
            [InlineKeyboardButton(emojize(":world_map: Indicazioni", use_aliases=True), url="http://www.asparagorgo.info/dove-siamo/")],
            [InlineKeyboardButton("« Indietro", callback_data=str(RESTART)),
            InlineKeyboardButton("·Esci·", callback_data=str(ESC))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["dovesiamo_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=emojize(text, use_aliases=True),
            reply_markup=reply_markup,
            disable_web_page_preview = True
        )
        return LAST

    def contatti(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
            [InlineKeyboardButton(emojize(":globe_with_meridians: Sito web", use_aliases=True), url="http://www.asparagorgo.info/")],
            [InlineKeyboardButton(emojize(":bust_in_silhouette: Facebook", use_aliases=True), url="https://www.facebook.com/asparagorgo/"),
            InlineKeyboardButton(emojize(":camera: Instagram", use_aliases=True), url="https://www.instagram.com/asparagorgo/")],
            [InlineKeyboardButton(emojize(":envelope_with_arrow: Mandami un messaggio", use_aliases=True), callback_data=str(MSG))],
            [InlineKeyboardButton("« Indietro", callback_data=str(RESTART)),
            InlineKeyboardButton("·Esci·", callback_data=str(ESC))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["contatti_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=emojize(text, use_aliases=True),
            reply_markup=reply_markup,
            disable_web_page_preview = True
        )
        return LAST
    
    def pMessage(self, update, context):
        query = update.callback_query
        bot = context.bot
        keyboard = [
                    [
                        InlineKeyboardButton("« Indietro", callback_data=str(CONTACTS)),
                        InlineKeyboardButton("·Esci·", callback_data=str(ESC))
                    ]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.text["msg_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            text=emojize(text, use_aliases=True),
            reply_markup=reply_markup,
            disable_web_page_preview = True
        )
        return STATE1

    def end(self, update, context):
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over"""
        query = update.callback_query
        bot = context.bot
        text = self.text["end_text"]
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text
        )
        return ConversationHandler.END

    def registerToDispatcher(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('info', self.info)],

            states={
                    FIRST: [CallbackQueryHandler(self.programma, pattern='^' + str(PROGRAM) + '$'),
                            CallbackQueryHandler(self.menu, pattern='^' + str(MENU) + '$'),
                            CallbackQueryHandler(self.doveSiamo, pattern='^' + str(WHERE) + '$'),
                            CallbackQueryHandler(self.contatti, pattern='^' + str(CONTACTS) + '$'),
                            CallbackQueryHandler(self.end, pattern='^' + str(ESC) + '$')
                            ],
                    LAST: [CallbackQueryHandler(self.start_over, pattern='^' + str(RESTART) + '$'),
                            CallbackQueryHandler(self.end, pattern='^' + str(ESC) + '$'),
                            CallbackQueryHandler(self.pMessage, pattern='^' + str(MSG) + '$')
                            ],
                    STATE1: [CallbackQueryHandler(self.contatti, pattern='^' + str(CONTACTS) + '$'),
                            CallbackQueryHandler(self.end, pattern='^' + str(ESC) + '$')
                            ]
            },

            fallbacks=[CommandHandler('info', self.info)],
            persistent=True, name='info_persistence'
        )
        self.dp.add_handler(conv_handler)

