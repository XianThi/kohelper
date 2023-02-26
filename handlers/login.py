from telebot import types, TeleBot
import utils
import time


class LoginHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        answer = f'Oyuna giriş işlemi başlatılıyor...\n{utils.OpenLauncher()}'
        self._bot.send_message(message.chat.id,answer)
        time.sleep(1)
        answer = utils.LoginKO()
        self._bot.send_message(message.chat.id,answer)
        if 'Sunucu seçiniz' in answer:
            btns_arr = {'Agartha':'server:agartha','Zero':'server:zero'}
            markup = utils.gen_markup(btns_arr)
            self._bot.send_message(message.chat.id,f"<i><b>Sunucu Seçimi:</b></i>\n\n\nLütfen sunucu seçin.", reply_markup=markup,parse_mode='html')