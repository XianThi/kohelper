from telegrambot import *

token = ""
chat_id = 0
botSettings = BotSettings(token,chat_id)
bot = TelegramBot(botSettings)
#bot.start_bot()
botThread = threading.Thread(target=bot.start_bot, daemon=True)
botThread.start()
while True:
    pass
