from telebot import types, TeleBot
import utils


class SS1080Handler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        photo=open(utils.SS1080(), "rb")
        self._bot.send_photo(message.chat.id,photo)