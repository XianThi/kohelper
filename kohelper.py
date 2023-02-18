import requests
from python_imagesearch.imagesearch import *
import win32gui
from time import sleep
import ocr

class KoHelper:
    def __init__(self):
        self.found_window = False
        self.chat_id = -651913034
        self.token = "6071564266:AAHjzBD5Wk3_Ot7AtAg7tcfCrrRpkks59TQ"
        self.api = "https://api.telegram.org/bot"
        self.bot_loop()
        self.disconnect = False
    def _input(self,message, input_type=str):
        while True:
            try:
                return input_type (input(message))
            except:
                pass
    def imagesearch_count(image, precision=0.9):
        img_rgb = pyautogui.screenshot()
        if is_retina:
            img_rgb.thumbnail((round(img_rgb.size[0] * 0.5), round(img_rgb.size[1] * 0.5)))
        img_rgb = np.array(img_rgb)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        count = []
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) // Uncomment to draw boxes around found occurrences
            count .append((pt[0], pt[1]))
        # cv2.imwrite('result.png', img_rgb) // Uncomment to write output image with boxes drawn around occurrences
        return count
    def get_name(self,x,y,width,height):
        screen_capture = ImageGrab.grab(bbox=x,y,x+width,y+height)
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
            dead_cnt = self.imagesearch_count("hpbar.png")
            if len(dead_cnt) > 0:
                x_count_list = []
                y_count_list = []

                for (x_count, y_count) in dead_cnt : 
                    x_count_list.append(x_count)
                    y_count_list.append(y_count)
            for i in range(0,len(dead_cnt)):
                name = self.get_name(self,x_count_list[i]+16,y_count_list[i]+25,95,14)
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
