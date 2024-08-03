from python_imagesearch.imagesearch import *
import win32gui
from time import sleep
from PIL import ImageGrab
import ocr
import threading
import json
import argparse

class RepairAndSell:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("--chat_id", help="Telegram Chat ID")
        parser.add_argument("--token",  help="Bot Token")
        parser.add_argument("--vipbag",  help="VIP Bag")
        args = parser.parse_args()
        config = vars(args)
        self.disconnect = False
        if config["chat_id"]!=None:
            self.chat_id = config["chat_id"]
        else:
            self.chat_id = -864786044
        if config["token"]!=None:
            self.token = config["token"]
        else:
            self.token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
        if config["vipbag"]!=None:
            self.vipbag = config["vipbag"]
        else:
            self.vipbag = "yok"
    
    def repair_kontrol(self)->None:
        while not self.disconnect:
            print("repair kontrolü çalışıyor..")
            #repair icin gerekli falliyetleri yap.
            sleep(600)
    
    def inventory_kontrol(self)->None:
        while not self.disconnect:
            print("sell kontrolü çalışıyor..")
            #inventory dolmus mu kontrol et
                #vipbag var mı yok mu kontrol et
                    #vipbagde yer var mı yok mu kontrol et 
                        #yer varsa itemleri inventoryden vipye gönder.
                    #yer yoksa
                        #town at itemleri sat
                #yoksa
                    #town at itemleri sat
            #dolmamışsa devam et
            sleep(600)

    def town(self):
        #town at
        return

    def repair_weapon(self):
        #silah tamiri
        return
    
    def sell_trash_items(self):
        #cöp itemleri sat
        return
    
    def check_vip_items(self):
        #vipdeki itemleri kontrol et
        #eğer atılacaksa al at
        return
    def inventory_to_vip(self,inv_pos):
        #inventoryden vipe at
        return
    def vip_to_inventory(self,vip_pos):
        #vipden inventorye cek
        return
    def sell_item(self,item_pos):
        #npcye sat
        return

if __name__ == "__main__":
    rs = RepairAndSell()
    x = threading.Thread(target=rs.repair_kontrol, daemon=True)
    x.start()
    sleep(1)
    y = threading.Thread(target=rs.inventory_kontrol, daemon=True)
    y.start()
    sleep(1)
    while True:
        pass