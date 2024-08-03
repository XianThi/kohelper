from telebot import types, TeleBot
import utils


class CaptchaHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        answer = utils.captcha(message,self._bot)
        self._bot.send_message(message.chat.id,answer,)
        answer = utils.LoginTamamla()
        self._bot.send_message(message.chat.id,answer,)