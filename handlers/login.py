from telebot import types, TeleBot
import utils


class LoginHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        answer = f'Oyuna giriş işlemi başlatılıyor...\n{utils.OpenLauncher()}'
        self._bot.send_message(message.chat.id,answer)
