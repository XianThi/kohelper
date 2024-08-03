import requests
from python_imagesearch.imagesearch import *
import win32gui
from time import sleep
from PIL import ImageGrab
import ocr
import threading
import json
import argparse

class KoHelper:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("--chat_id", help="Telegram Chat ID")
        parser.add_argument("--token",  help="Bot Token")
        parser.add_argument("--partidcms",  default=30, type=int, help="parti dc kontrol süresi")
        parser.add_argument("--olumms",  default=30, type=int, help="ölüm kontrol süresi")
        parser.add_argument("--dcms",  default=300, type=int, help="ölüm kontrol süresi")
        parser.add_argument("--nation",  default=2, type=int, help="ırk bilgisi")
        parser.add_argument("--wrcount",  default=2,type=int, help="Partide kaç warrior var?")
        parser.add_argument("--rgcount",  default=2,type=int, help="Partide kaç rogue var?")
        parser.add_argument("--prcount",  default=2,type=int, help="Partide kaç priest var?")
        parser.add_argument("--mgcount",  default=2,type=int, help="Partide kaç mage var?")
        args = parser.parse_args()
        config = vars(args)
        print(config)
        self.found_window = False
        self.disconnect = False
        self.api = "https://api.telegram.org/bot"
        #self.getUpdates()
        self.sizes = (0,0,0,0)
        if config["partidcms"]!=None:
            self.parti_dc_time = config["partidcms"]
        else:
            self.parti_dc_time = self._input("Parti DC kontrol süresi (sn)?\r\n",int)
        if config["olumms"]!=None:
            self.olum_time = config["olumms"]
        else:
            self.olum_time = self._input("Ölüm kontrol süresi (sn)?\r\n",int)
        if config["dcms"]!=None:
            self.dc_time = config["dcms"]
        else:
            self.dc_time = self._input("DC kontrol süresi (sn)?\r\n",int)
        if config["nation"]!=None:
            self.humankarus = config["nation"]
        else:
            self.humankarus = self._input("1-Human\r\n2-Karus\r\n",int)
        if config["chat_id"]!=None:
            self.chat_id = config["chat_id"]
        else:
            self.chat_id = -864786044
        if config["token"]!=None:
            self.token = config["token"]
        else:
            self.token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
        if self.humankarus == 1 :
            self.tip = "human"
        else:
            self.tip = "karus"
        
        if config["wrcount"]!=None:
            self.warrior = config["wrcount"]
        else:
            self.warrior = self._input("Partide kaç adet warrior var?\r\n",int)
        if config["rgcount"]!=None:
            self.rogue = config["rgcount"]
        else:
            self.rogue = self._input("Partide kaç adet rogue var?\r\n",int)
        if config["prcount"]!=None:
            self.priest = config["prcount"]
        else:
            self.priest = self._input("Partide kaç adet priest var?\r\n",int)
        if config["mgcount"]!=None:
            self.mage = config["mgcount"]
        else:
            self.mage = self._input("Partide kaç adet mage var?\r\n",int)
        print("\n[!] Oyun penceresi aranıyor..\r\n")
        while not self.found_window:
            print("  pencere bulunamadı tekrar deneniyor..")
            win32gui.EnumWindows(self.callback, None)
            sleep(1)
        print("\n[!] Pencere bulundu. Bot baslatılıyor lütfen pencereye geçiş yapınız.")
        sleep(2)
        
    def _input(self,message, input_type=str):
        while True:
            try:
                return input_type (input(message))
            except:
                pass

    def getUpdates(self):
        print("\n[!!!] Lütfen kanalınızın ID'sini güncelleyiniz.\r\n")
        print("\n[!!!] KANAL LISTESI [!!!!]")
        url = f"{self.api}{self.token}/getUpdates"
        json = requests.get(url).json()
        for i in json["result"] :
            if i.__contains__("message"):
                if i["message"]["chat"].__contains__("title"):
                    kanal = i["message"]["chat"]["title"]
                else:
                    kanal = i["message"]["chat"]["username"]
                kanal_id = i["message"]["chat"]["id"]
                print (f"{kanal} - {kanal_id}")
        print("\r\n\r\n")
    
    def get_name(self,x,y,width,height):
        screen_capture = ImageGrab.grab(bbox=(x,y,x+width,y+height))
        name: str = ocr.get_text_from_image(image=screen_capture)
        return name
    
    def callback(self,hwnd, extra) -> None:  # pylint: disable=unused-argument
        """Function used to find the game window and get its size"""
        if "Knight OnLine Client" not in win32gui.GetWindowText(hwnd):
            return
        rect = win32gui.GetWindowRect(hwnd)
        x_pos = rect[0]
        y_pos = rect[1]
        width = rect[2] - x_pos
        height = rect[3] - y_pos
        print(f"  {win32gui.GetWindowText(hwnd)} bulundu.")
        print(f"    Konum: ({x_pos}, {y_pos})")
        print(f"    Boyut:     ({width}, {height})")
        self.sizes = (x_pos,y_pos,width,height)
        self.found_window = True   

    def search(self,tip,job):
        count = imagesearch_count("images/"+tip+job+".png")
        return count

    def sendMessage(self,msg):
        print("\n[!!!]"+msg)
        url = f"{self.api}{self.token}/sendMessage?chat_id={self.chat_id}&text={msg}"
        requests.get(url)

    def olen_var_mi(self)->None:
        while not self.disconnect:
            print("Parti ölüm kontrolü çalışıyor..")
            dead_cnt = imagesearch_count_ex("./images/hpbar.png")
            if len(dead_cnt) > 0:
                x_count_list = []
                y_count_list = []
                for (x_count, y_count) in dead_cnt:
                    x_count_list.append(x_count)
                    y_count_list.append(y_count)
            for i in range(0,len(dead_cnt)):
                name = self.get_name(x_count_list[i]+16,y_count_list[i]+25,95,14)
                mesaj = f"{name} öldü. Lütfen çarı diriltin."
                self.sendMessage(mesaj)
            sleep(self.olum_time)

    def dc(self)->None:
        while not self.disconnect:
            print("Karakter DC kontrolü çalışıyor..")
            text = ocr.get_text(self.sizes,1,1)
            if "Disconnected from server" in text:
                self.disconnect = True
                print("DC oldunuz.")
            sleep(self.dc_time)
    
    def dc_olan_var_mi(self)->None:
        while not self.disconnect:
            print("Parti dc kontrolü çalışıyor..")
            warrior_cnt = self.search(self.tip,"warrior")
            rogue_cnt = self.search(self.tip,"rogue")
            priest_cnt = self.search(self.tip,"priest")
            mage_cnt = self.search(self.tip,"mage")
            if warrior_cnt<self.warrior:
                eksik = self.warrior-warrior_cnt
                mesaj = f"Partide {eksik} warrior eksik"
                self.sendMessage(mesaj)              
            if rogue_cnt<self.rogue:
                eksik = self.rogue-rogue_cnt
                mesaj = f"Partide {eksik} rogue eksik"
                self.sendMessage(mesaj)
            if priest_cnt<self.priest:
                eksik = self.priest-priest_cnt
                mesaj = f"Partide {eksik} priest eksik"
                self.sendMessage(mesaj)
            if mage_cnt<self.mage:
                eksik = self.mage-mage_cnt
                mesaj = f"Partide {eksik} mage eksik"
                self.sendMessage(mesaj)
            sleep(self.parti_dc_time)


if __name__ == "__main__":
    helper = KoHelper()
    dc_olan_kontrol = threading.Thread(target=helper.dc_olan_var_mi, daemon=True)
    dc_olan_kontrol.start()
    sleep(1)
    olen_kontrol = threading.Thread(target=helper.olen_var_mi, daemon=True)
    olen_kontrol.start()
    sleep(1)
    dc_kontrol = threading.Thread(target=helper.dc, daemon=True)
    dc_kontrol.start()
    sleep(1)
    while True:
        pass