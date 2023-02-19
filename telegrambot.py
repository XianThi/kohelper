import json
from telebot import types, TeleBot
import requests
import threading
import utils
from handlers.start import StartHandler
from handlers.info import InfoHandler
from handlers.ss1080 import SS1080Handler
from handlers.login import LoginHandler

class BotSettings:
    
    def __init__(self,token,chat_id):
        self.chat_id = chat_id
        self.token = token
    
    def getToken(self):
        return self.token
    def getChatId(self):
        return self.chat_id

class TelegramBot:
    def __init__(self, botSettings:BotSettings) -> None:
        self.token = botSettings.getToken()
        self.chat_id = botSettings.getChatId()
        self.bot = None
        self.set_bot()
    
    def set_bot(self) -> None:
        self.bot = TeleBot(self.token,parse_mode="HTML")
        self.bot.set_my_commands([
            types.BotCommand("/start", "doing nothing"),
            types.BotCommand("/info", "Get PC Info"),
            types.BotCommand("/ss1080", "Get 1080p Screenshot"),
            types.BotCommand("/login", "Login to game"),
            types.BotCommand("/mottock", "Start mottock"),
        ])
        self.register_handlers()

    def register_handlers(self) -> None:
        self.bot.register_message_handler(StartHandler, commands=["start"], pass_bot=True)
        self.bot.register_message_handler(InfoHandler, commands=["info"], pass_bot=True)
        self.bot.register_message_handler(SS1080Handler, commands=["ss1080"], pass_bot=True)
        self.bot.register_message_handler(LoginHandler, commands=["login"], pass_bot=True)
    
    def start_bot(self):
        print("bot baslatiliyor..")
        self.bot.infinity_polling()
