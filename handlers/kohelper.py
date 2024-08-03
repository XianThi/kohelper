from telebot import types, TeleBot
from telebot.handler_backends import ContinueHandling
import utils

class KOHelperHandler:    
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self.first(message)

    def first(self, message: types.Message) -> None:
        btns_arr = {'10 sn': 'partidcms:10', '30 sn':'partidcms:30', '1 dk': 'partidcms:60', '5 dk':'partidcms:300', '10 dk':'partidcms:600', '30 dk':'partidcms:1800', '1 sa':'partidcms:3600'}
        markup = utils.gen_markup(btns_arr)
        self._bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Parti DC kontrol süresi (sn)?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def stepone(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'10 sn': 'olumms:10', '30 sn':'olumms:30', '1 dk': 'olumms:60', '5 dk':'olumms:300', '10 dk':'olumms:600', '30 dk':'olumms:1800', '1 sa':'olumms:3600'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Ölüm kontrol süresi (sn)?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def steptwo(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'10 sn': 'dcms:10', '30 sn':'dcms:30', '1 dk': 'dcms:60', '5 dk':'dcms:300', '10 dk':'dcms:600', '30 dk':'dcms:1800', '1 sa':'dcms:3600'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>DC kontrol süresi (sn)?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def stepthree(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'Human': 'nation:1', 'Karus':'nation:2'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Human ya da Karus?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def stepfour(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'0':'wrcount:0','1': 'wrcount:1', '2':'wrcount:2','3': 'wrcount:3', '4':'wrcount:4','5': 'wrcount:5', '6':'wrcount:6','7': 'wrcount:7', '8':'wrcount:8'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Partide kaç adet warrior var?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def stepfive(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'0':'rgcount:0','1': 'rgcount:1', '2':'rgcount:2','3': 'rgcount:3', '4':'rgcount:4','5': 'rgcount:5', '6':'rgcount:6','7': 'rgcount:7', '8':'rgcount:8'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Partide kaç adet rogue var?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def stepsix(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'0':'prcount:0','1': 'prcount:1', '2':'prcount:2','3': 'prcount:3', '4':'prcount:4','5': 'prcount:5', '6':'prcount:6','7': 'prcount:7', '8':'prcount:8'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Partide kaç adet priest var?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
        
    def stepseven(message:types.Message,bot:TeleBot)->None:
        btns_arr = {'0':'mgcount:0','1': 'mgcount:1', '2':'mgcount:2','3': 'mgcount:3', '4':'mgcount:4','5': 'mgcount:5', '6':'mgcount:6','7': 'mgcount:7', '8':'mgcount:8'}
        markup = utils.gen_markup(btns_arr)
        bot.send_message(message.chat.id,f"<i><b>KOHelper Ayarları</b></i>\n\n\n<b>Partide kaç adet mage var?</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    def bot_started(message:types.Message,bot:TeleBot)->None:
        bot.send_message(message.chat.id,f"KOHelper başlatıldı.")
        return ContinueHandling()