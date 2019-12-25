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

    def createImg(self, text, textsize):
        '''
        Given a text (string) and its font size (textsize, int),
        returns a base image with the given text written on it 
        '''
        # add newlines to text after line_length characters
        line_length = 24
        text = textwrap.fill(text, line_length, replace_whitespace=False)

        # get the base image
        base = Image.open('./images/base.jpg').convert('RGBA')

        # get a font
        # fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', textsize)
        fnt = ImageFont.truetype('fonts/OpenSansEmoji.ttf', textsize, encoding='unicode')

        # get a drawing context
        d = ImageDraw.Draw(base)

        # select a box to write on (top left and bottom right corners)
        bounding_box = [110, 500, 630, 640]
        x1, y1, x2, y2 = bounding_box  # for easy reading

        # calculate the width and height of the text to be drawn, given font size
        w, h = d.textsize(text, font=fnt)

        # Calculate the mid points and offset by the upper left corner of the bounding box
        x = (x2 - x1 - w)/2 + x1
        y = (y2 - y1 - h)/2 + y1

        # write the text to the image, where (x,y) is the top left corner of the text
        d.text((x, y), text, (0,0,0), align='center', font=fnt)
        # # FOR TESTING draw the bounding box to show that this works
        # d.rectangle([x1, y1, x2, y2])
        
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
        
        if len(text) <= 84:
            self.createImg(text, 40)
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

