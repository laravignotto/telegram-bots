from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import telegram
from emoji import emojize
import os
import random

class DancanText:
    '''
    Sends a pseudo random text message given a text file
    containing an original text
    '''
    dp = None

    def __init__(self, parent, dispatcher):
        assert(parent.isBot())
        assert(dispatcher!=None)
        self.dp = dispatcher
        # open the file containing the original text
        file_ = open("src/dancan_msgs.txt")
        # create the object
        self.markov = self.Markov(file_)

    def dancanText(self, update, context):
        chat_id = update.message.chat_id
        size = random.randrange(8, 40)
        text = self.markov.generate_markov_text(size)
        try:
            fullstop_idx = text.rindex(".")
            text = text[:fullstop_idx+1]
        except ValueError:
            pass

        context.bot.send_message(chat_id=chat_id, 
                    text=emojize(":crystal_ball: Dancan dice: :crystal_ball:\n" + text, use_aliases=True),
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    )

    def registerToDispatcher(self):
        self.dp.add_handler(CommandHandler('dancantext', self.dancanText))

    # code below taken from:
    # https://www.agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
    class Markov(object):
        def __init__(self, open_file):
            self.cache = {}
            self.open_file = open_file
            self.words = self.file_to_words()
            self.word_size = len(self.words)
            self.database()
            
        def file_to_words(self):
            self.open_file.seek(0)
            data = self.open_file.read()
            words = data.split()
            return words
            
        def triples(self):
            ''' 
            Generates triples from the given data string. So if our string were
            "What a lovely day", we'd generate (What, a, lovely) and then
            (a, lovely, day).
            '''
            if len(self.words) < 3:
                return
            
            for i in range(len(self.words) - 2):
                yield (self.words[i], self.words[i+1], self.words[i+2])
                
        def database(self):
            for w1, w2, w3 in self.triples():
                key = (w1, w2)
                if key in self.cache:
                    self.cache[key].append(w3)
                else:
                    self.cache[key] = [w3]
                    
        def generate_markov_text(self, size=18):
            seed = random.randint(0, self.word_size-3)
            seed_word, next_word = self.words[seed], self.words[seed+1]
            w1, w2 = seed_word, next_word
            gen_words = []
            for i in range(size):
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
            return ' '.join(gen_words)


