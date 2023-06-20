from FuncsForSPO.flanguage.translator.base import *

class Translator(BotMain):
    def __init__(self, text, lang_from, lang_to):
        self.TEXT = text
        self.LANG_FROM = lang_from
        self.LANG_TO = lang_to
        self.HEADLESS = headless
        self.CREDENTIALS = credentials
        super().__init__(self.HEADLESS)
        
