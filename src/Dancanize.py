from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import telegram
import requests
# import re
from emoji import emojize
import os
import json
from PIL import Image
from PIL import ImageDraw, ImageFont
import textwrap

class Dancanize:
    dp = None
    
    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher
        self.text = json.load(open("src/dancanize_texts.json"))

    def createImg(self, text, textsize, starting_point, line_length):
        '''
        Given a text (string), its font size (int), the starting point in
        the image (tuple of ints), and the max length of a line of text 
        (int), returns a base image with the given text written on it 
        '''
        text = textwrap.fill(text, line_length, replace_whitespace=False)
        # get the base image
        base = Image.open('./images/base.jpg').convert('RGBA')
        # get a font
        # fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', textsize)
        fnt = ImageFont.truetype('fonts/OpenSansEmoji.ttf', textsize, encoding='unicode')
        # get a drawing context
        d = ImageDraw.Draw(base)
        # draw text
        d.multiline_text(starting_point, text, (0,0,0), font=fnt, align='center')
        # save image
        base.save('images/result.png')

    def dancanize(self, update, context):
        '''
        sends an image with text
        '''
        chat_id = update.message.chat_id

        # get desired text (reply to message with the /dancanize command)
        try:
            text = emojize(update.message.reply_to_message.text, use_aliases=True)
        except:
            context.bot.send_message(chat_id=chat_id,
                                    text=emojize(self.text["wrong_use"], use_aliases=True),
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        
        # the text can't be too long (e.g. it has to occupy a desired space)
        if (len(text) <= 24) and (text.count('\n') <= 1):
            textsize = 42
            starting_point = (120,530)
            line_length = 25
            self.createImg(text, textsize, starting_point, line_length)
            # send the image
            photo = open('./images/result.png', 'rb')
            context.bot.send_photo(chat_id=chat_id, 
                                    photo=photo,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        elif (24 < len(text) < 95) and (text.count('\n') <= 2):
            textsize = 36
            starting_point = (110,510)
            line_length = 34
            self.createImg(text, textsize, starting_point, line_length)
            # send the image
            photo = open('./images/result.png', 'rb')
            context.bot.send_photo(chat_id=chat_id, 
                                    photo=photo,
                                    parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            context.bot.send_message(chat_id=chat_id,
                                    text=emojize(self.text["text_too_long"], use_aliases=True),
                                    parse_mode=telegram.ParseMode.MARKDOWN)

    def registerToDispatcher(self):
        self.dp.add_handler(CommandHandler('dancanize', self.dancanize))

