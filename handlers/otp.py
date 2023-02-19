from telebot import types, TeleBot
import utils
import time


class OTPHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        answer = utils.EnterOTP('123456')
        self._bot.send_message(message.chat.id,answer)
        markup = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton('ZERO', callback_data='ZERO')
        item_no = types.InlineKeyboardButton('AGARTA', callback_data='AGARTA')
        markup.row(item_yes, item_no)
        self._bot.send_message(message.chat.id,f"<i><b>Sunucu Seçimi:</b></i>\n\n\nLütfen sunucu seçin.", reply_markup=markup,
                 parse_mode='html')