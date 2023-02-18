import requests
from python_imagesearch.imagesearch import *
import win32gui
from time import sleep
from PIL import ImageGrab
import ocr

class KoHelper:
    def __init__(self):
        self.found_window = False
        self.chat_id = -644166565
        self.token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
        self.api = "https://api.telegram.org/bot"
        self.disconnect = False
        self.getUpdates()
        self.bot_loop()
        
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
        self.found_window = True   

    def search(self,tip,job):
        count = imagesearch_count("images/"+tip+job+".png")
        return count

    def sendMessage(self,msg):
        print("\n[!!!]"+msg)
        url = f"{self.api}{self.token}/sendMessage?chat_id={self.chat_id}&text={msg}"
        requests.get(url)

    def bot_loop(self)->None:
        humankarus = self._input("1-Human\r\n2-Karus\r\n",int)
        if humankarus == 1 :
            tip = "human"
        else:
            tip = "karus"
        warrior = self._input("Partide kaç adet warrior var?\r\n",int)
        rogue = self._input("Partide kaç adet rogue var?\r\n",int)
        priest = self._input("Partide kaç adet priest var?\r\n",int)
        mage = self._input("Partide kaç adet mage var?\r\n",int)
        print("\n[!] Oyun penceresi aranıyor..\r\n")
        while not self.found_window:
            print("  pencere bulunamadı tekrar deneniyor..")
            win32gui.EnumWindows(self.callback, None)
            sleep(2)
        print("\n[!] Pencere bulundu. Bot baslatılıyor lütfen pencereye geçiş yapınız.")
        sleep(2)
        while not self.disconnect:
            dead_cnt = imagesearch_count_ex("./images/hpbar.png")
            if len(dead_cnt) > 0:
                x_count_list = []
                y_count_list = []

                for (x_count, y_count) in dead_cnt : 
                    x_count_list.append(x_count)
                    y_count_list.append(y_count)
            for i in range(0,len(dead_cnt)):
                name = self.get_name(x_count_list[i]+16,y_count_list[i]+25,95,14)
                mesaj = f"{name} öldü. Lütfen çarı diriltin."
                self.sendMessage(mesaj)
            warrior_cnt = self.search(tip,"warrior")
            rogue_cnt = self.search(tip,"rogue")
            priest_cnt = self.search(tip,"priest")
            mage_cnt = self.search(tip,"mage")
            if warrior_cnt<warrior:
                eksik = warrior-warrior_cnt
                mesaj = f"Partide {eksik} warrior eksik"
                self.sendMessage(mesaj)
            if rogue_cnt<rogue:
                eksik = rogue-rogue_cnt
                mesaj = f"Partide {eksik} rogue eksik"
                self.sendMessage(mesaj)
            if priest_cnt<priest:
                eksik = priest-priest_cnt
                mesaj = f"Partide {eksik} priest eksik"
                self.sendMessage(mesaj)
            if mage_cnt<mage:
                eksik = mage-mage_cnt
                mesaj = f"Partide {eksik} mage eksik"
                self.sendMessage(mesaj)
            sleep(10)


if __name__ == '__main__':
    KoHelper()
