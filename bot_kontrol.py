from telegrambot import *

token = "6071564266:AAEHuIFfE4lxLFdlQa61U0fJhVZbRBZze4g"
chat_id = -864786044
botSettings = BotSettings(token,chat_id)
bot = TelegramBot(botSettings)
#bot.start_bot()
botThread = threading.Thread(target=bot.start_bot, daemon=True)
botThread.start()
while True:
    pass