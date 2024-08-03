from telebot import types, TeleBot
import utils


class RestartHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        utils.restart_pc()
        self._bot.send_message(message.chat.id, "Bilgisayar yeniden başlatılıyor.",)