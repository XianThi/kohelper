import argparse
import threading
from time import sleep
import win32gui
import pydirectinput
import os
import base64
import win32clipboard
import interception


class ShoutMessage:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("--message", help="Message")
        parser.add_argument("--client", help="Client Title")
        parser.add_argument("--interception", help="Use Interception Method")
        args = parser.parse_args()
        config = vars(args)
        self.timeout=30
        if config["message"]!=None:
            self.message = self.decodeBase64(config["message"])
        else:
            exit
        self.found_window = False
        self.repeat = 0
        if config["client"]!=None:
            self.client = self.decodeBase64(config["client"])
        else:
            self.client = "Knight OnLine Client"
        if config["interception"]!=None:
            self.interception = True
        else:
            self.interception = False
        while not self.found_window:
            print("  pencere bulunamadı tekrar deneniyor..")
            win32gui.EnumWindows(self.callback, None)
            sleep(1)
        print("\n[!] Pencere bulundu. Bot baslatılıyor lütfen pencereye geçiş yapınız.")
        sleep(2)
    
    def decodeBase64(self,text):
        base64_bytes = text.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
    
    def set_clipboard(self,text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
    
    def send_msg(self):
        if self.interception:
            interception.press("enter")
            with interception.hold_key("ctrl"):
                interception.press("v")
            interception.press("enter")
        else:
            pydirectinput.keyDown('enter')
            pydirectinput.keyUp('enter')
            pydirectinput.keyDown('ctrl')
            pydirectinput.keyDown('v')
            pydirectinput.keyUp('ctrl')
            pydirectinput.keyUp('v')
            pydirectinput.keyDown('enter')
            pydirectinput.keyUp('enter')
        
    
    def callback(self,hwnd, extra) -> None:  # pylint: disable=unused-argument
        """Function used to find the game window and get its size"""
        if self.client not in win32gui.GetWindowText(hwnd):
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

    def shout(self)->None:
        while True:
            mesaj = self.message
            if self.repeat>1:
                mesaj += mesaj
                self.repeat = 0
            self.set_clipboard(mesaj)
            print(f"Mesaj gönderiliyor : {self.message}")
            self.send_msg()
            self.repeat =  self.repeat + 1
            sleep(self.timeout)
        
if __name__ == "__main__":
    shoutMessage = ShoutMessage()
    shout_thread = threading.Thread(target=shoutMessage.shout, daemon=True)
    shout_thread.start()
    #sleep(1)
    while True:
        pass