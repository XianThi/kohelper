from telegrambot import *

token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
chat_id = -864786044
botSettings = BotSettings(token,chat_id)
bot = TelegramBot(botSettings)
bot.start_bot()