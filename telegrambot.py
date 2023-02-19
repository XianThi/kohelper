from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import asyncio
import json
import requests
import threading
import utils


class BotSettings:
    
    def __init__(self,token,chat_id):
        self.chat_id = chat_id
        self.token = token
    
    def getToken(self):
        return self.token
    def getChatId(self):
        return self.chat_id

class TelegramBot:
    fsm_basic_storage = 'memory'
    def __init__(self, botSettings:BotSettings, storage_type: str = fsm_basic_storage) -> None:
        self.token = botSettings.getToken()
        self.chat_id = botSettings.getChatId()
        self.storage_type = storage_type
        self.bot = None
        self.dispatcher = None
        self.set_bot()
        self.set_dispatcher()
    
    def set_bot(self) -> None:
        self.bot = Bot(token=self.token,parse_mode=types.ParseMode.HTML)
        
    def set_dispatcher(self) -> None:
        if self.storage_type == self.__class__.fsm_basic_storage:
            self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())
        else:
            # TODO: migrate to db type of storage
            pass
    def register_handlers(self,disp: Dispatcher) -> None:
        disp.register_message_handler(self.cmd_start, commands=['start'])
        disp.register_message_handler(self.cmd_info, commands=['info'])
        disp.register_message_handler(self.cmd_ss1080, commands=['ss1080'])
    
    def start_bot(self):
        self.register_handlers(self.dispatcher)
        executor.start_polling(self.dispatcher, skip_updates=True)
    
    async def send_message(self,msg)->None:
        msg = "*"+msg+"*"
        print(msg)
        await self.bot.send_message(self.chat_id,msg)
        
    async def cmd_start(self,message: types.Message) -> None:
        answer = f'Güncellenecek!'
        await message.answer(text=answer)

    async def cmd_ss1080(self,message: types.Message)->None:
        photo=open(utils.SS1080(), "rb")
        await self.bot.send_photo(message.chat.id,photo)

    async def cmd_info(self,message: types.Message) -> None:
        answer = f'\n\n<pre><b>🖥 PC Name</b> -> {utils.PC_Name()}\n\n=============== Boot Time ===============\n<b>🕛 Uptime</b> -> {utils.Uptime()} | {utils.today()} </pre>\n\n'
        answer = answer + f'<pre>=============== CPU Info ===============\n<b>📊 Total Core : </b> {utils.CPU_Count()} | <b>📈 Current Usage :</b> %{utils.CPU_Usage()} </pre>\n\n'
        answer = answer + f'<pre>=============== Memory Info ===============\n<b>🛑 Total RAM : </b> {utils.Total_RAM()} | <b>⭕️ Free RAM :</b> {utils.Free_RAM()} </pre>\n\n'
        answer = answer + f'<pre>=============== HDD/SSD Info ===============\n<b>📁 Total HDD : </b> {utils.Total_HDD()} | <b>📂 Free HDD :</b> {utils.Free_HDD()} </pre>\n\n'
        answer = answer + f'<pre>=============== Region / IP Info ===============\n<b>🌎 Region : </b> {utils.Location()} | <b>📌 IP Address :</b> {utils.IP_Address()} </pre>\n\n'
        await message.answer(text=answer)