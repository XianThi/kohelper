from telebot import types, TeleBot
import utils


class LoginHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        self._bot.send_message(message.chat.id,"Oyuna giriş işlemi başlatılıyor..")