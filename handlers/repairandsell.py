from telebot import types, TeleBot
from telebot.handler_backends import ContinueHandling
import utils


class RepairAndSellHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)
    def _handle(self, message: types.Message) -> None:
        #self._bot.send_message(message.chat.id, "Güncellenecek elbet bir gün",)
        self.status(message)
    
    def status(self, message: types.Message) -> None:
        btns_arr = {'Aktif':'repairandsell:active','Pasif':'repairandsell:deactive'}
        markup = utils.gen_markup(btns_arr)
        self._bot.send_message(message.chat.id,f"<i><b>Rpr ve Sell Durumu</b></i>\n\n\n<b>Aktif veya Pasif olarak seçin.</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()
    
    def VIPBag(self,message):
        btns_arr = {'Var':'vipbag:var','Yok':'vipbag:yok'}
        markup = utils.gen_markup(btns_arr)
        self._bot.send_message(message.chat.id,f"<i><b>VIPBag Durumu</b></i>\n\n\n<b>Var veya Yok olarak seçin.</b>\r\n", reply_markup=markup,parse_mode='html')
        return ContinueHandling()