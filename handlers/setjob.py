from telebot import types, TeleBot
from telebot.handler_backends import ContinueHandling
import utils

class SetJobHandler:    
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        utils.setJob(message)
        self._bot.send_message(message.chat.id, "Job başarıyla kaydedildi.",)
    