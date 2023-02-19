from telegrambot import *

token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
chat_id = -864786044
botSettings = BotSettings(token,chat_id)
bot = TelegramBot(botSettings)
botThread = threading.Thread(target=bot.start_bot, daemon=True)
botThread.start()
while True:
    pass