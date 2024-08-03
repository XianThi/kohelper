from telebot import types, TeleBot
import utils

class InfoHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        answer = f'\n\n<pre><b>🖥 PC Name</b> -> {utils.PC_Name()}\n\n=============== Boot Time ===============\n<b>🕛 Uptime</b> -> {utils.Uptime()} | {utils.today()} </pre>\n\n'
        answer = answer + f'<pre>=============== CPU Info ===============\n<b>📊 Total Core : </b> {utils.CPU_Count()} | <b>📈 Current Usage :</b> %{utils.CPU_Usage()} </pre>\n\n'
        answer = answer + f'<pre>=============== Memory Info ===============\n<b>🛑 Total RAM : </b> {utils.Total_RAM()} | <b>⭕️ Free RAM :</b> {utils.Free_RAM()} </pre>\n\n'
        answer = answer + f'<pre>=============== HDD/SSD Info ===============\n<b>📁 Total HDD : </b> {utils.Total_HDD()} | <b>📂 Free HDD :</b> {utils.Free_HDD()} </pre>\n\n'
        answer = answer + f'<pre>=============== Region / IP Info ===============\n<b>🌎 Region : </b> {utils.Location()} | <b>📌 IP Address :</b> {utils.IP_Address()} </pre>\n\n'
        self._bot.send_message(message.chat.id,answer)