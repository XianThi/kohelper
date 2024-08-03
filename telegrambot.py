import json
from telebot import types, TeleBot
import requests
import threading
import utils
from handlers.start import StartHandler
from handlers.info import InfoHandler
from handlers.ss1080 import SS1080Handler
from handlers.login import LoginHandler
from handlers.otp import OTPHandler
from handlers.kohelper import KOHelperHandler
from handlers.stopkohelper import StopKOHelperHandler
from handlers.startup import StartupHandler
from handlers.restart import RestartHandler
from handlers.captcha import CaptchaHandler
from handlers.repairandsell import RepairAndSellHandler
from handlers.setnick import SetNickHandler
from handlers.setjob import SetJobHandler
from handlers.setpos import SetPosHandler
from handlers.tp import TPHandler
from handlers.addtp import AddTPHandler
from handlers.deltp import DelTPHandler
from handlers.shout import ShoutHandler
from handlers.warprejoin import WarPreHandler
from handlers.roguemacrohandler import RogueMacroHandler
from handlers.primacrohandler import PriestMacroHandler
from utils import SunucuSecim,AltSunucuSecim,PartiDCMS,OlumMS,DCMS,Nation,WarriorCount,RogueCount,PriestCount,MageCount,RepairAndSell,VIPBag


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
        self.register_handlers()
    
    def set_bot(self) -> None:
        self.bot = TeleBot(self.token,parse_mode="HTML")
        self.bot.set_my_commands([
            types.BotCommand("/start", "Open Game Screen (use /start x for x minutes later)"),
            types.BotCommand("/info", "Get PC Info"),
            types.BotCommand("/startup", "Launch on windows startup"),
            types.BotCommand("/restart", "Restart PC"),
            types.BotCommand("/kohelper", "Start KOHelper"),
            types.BotCommand("/stop_kohelper", "Stop KOHelper"),
            types.BotCommand("/ss1080", "Get 1080p Screenshot"),
            types.BotCommand("/login", "Login to game"),
            types.BotCommand("/otp", "Enter OTP Code for Login"),
            types.BotCommand("/captcha", "Enter OTP Code for Login"),            
            types.BotCommand("/mottock", "Start mottock"),                   
            types.BotCommand("/repairandsell", "Active or deactive repair and sell process"),             
            types.BotCommand("/setnick", "Set nick"),           
            types.BotCommand("/setjob", "Set job"),            
            types.BotCommand("/setpos", "Set position of party"),                
            types.BotCommand("/addtplist", "Add a  character to TP List by pt position"),  
            types.BotCommand("/deltplist", "Delete a  character to TP List by pt position"),     
            types.BotCommand("/tp", "TP character from pt by pt position"),    
            types.BotCommand("/shout", "Write shout every 10 seconds"),
            types.BotCommand("/warprejoin", "Join War Pre Event"),
            types.BotCommand("/roguemacro", "Start Rogue Macro"),
            types.BotCommand("/priestmacro", "Start Priest Macro"),
        ])

    def register_handlers(self) -> None:
        command_handlers = {
        "start" : StartHandler,
        "info" : InfoHandler,
        "startup" : StartupHandler,
        "restart" : RestartHandler,
        "ss1080" : SS1080Handler,
        "login" : LoginHandler,
        "otp" : OTPHandler,
        "captcha" : CaptchaHandler,
        "kohelper":KOHelperHandler,
        "repairandsell":RepairAndSellHandler,
        "stop_kohelper": StopKOHelperHandler,
        "setnick": SetNickHandler,
        "setjob": SetJobHandler,
        "setpos": SetPosHandler,
        "addtplist": AddTPHandler,
        "deltplist": DelTPHandler,
        "tp": TPHandler,
        "shout": ShoutHandler,
        "warprejoin" : WarPreHandler,
        "roguemacro" : RogueMacroHandler,
        "priestmacro" : PriestMacroHandler,
        }
        for command, handler in command_handlers.items():
            self.bot.register_message_handler(handler, commands=[command], pass_bot=True)
        self.bot.register_callback_query_handler(SunucuSecim,func=lambda message:message.data.startswith("server"),pass_bot=True)
        self.bot.register_callback_query_handler(AltSunucuSecim,func=lambda message:message.data.startswith("altserver"),pass_bot=True)
        self.bot.register_callback_query_handler(PartiDCMS,func=lambda message:message.data.startswith('partidcms'),pass_bot=True)
        self.bot.register_callback_query_handler(OlumMS,func=lambda message:message.data.startswith('olumms'),pass_bot=True)
        self.bot.register_callback_query_handler(DCMS,func=lambda message:message.data.startswith('dcms'),pass_bot=True)
        self.bot.register_callback_query_handler(Nation,func=lambda message:message.data.startswith('nation'),pass_bot=True)
        self.bot.register_callback_query_handler(WarriorCount,func=lambda message:message.data.startswith('wrcount'),pass_bot=True)
        self.bot.register_callback_query_handler(RogueCount,func=lambda message:message.data.startswith('rgcount'),pass_bot=True)
        self.bot.register_callback_query_handler(PriestCount,func=lambda message:message.data.startswith('prcount'),pass_bot=True)
        self.bot.register_callback_query_handler(MageCount,func=lambda message:message.data.startswith('mgcount'),pass_bot=True)
        self.bot.register_callback_query_handler(RepairAndSell,func=lambda message:message.data.startswith('repairandsell'),pass_bot=True)
        self.bot.register_callback_query_handler(VIPBag,func=lambda message:message.data.startswith('vipbag'),pass_bot=True)

    def start_bot(self):
        print("bot baslatiliyor..")
        self.bot.infinity_polling()