from telegrambot import *

token = "6121032651:AAFUqApv1T4j23TaQCl0g4H4MPP8YA4kqV4"
chat_id = -864786044
botSettings = BotSettings(token,chat_id)
bot = TelegramBot(botSettings)
#bot.start_bot()
botThread = threading.Thread(target=bot.start_bot, daemon=True)
botThread.start()
while True:
    pass