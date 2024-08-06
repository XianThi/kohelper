import os
import datetime
import wmi
import multiprocessing
import psutil
import requests
import pyautogui
import base64
import pythoncom
import subprocess
import pydirectinput
from PIL import ImageGrab
import cv2
import pytesseract
import ctypes
from typing import Any
import numpy as np
from python_imagesearch.imagesearch import *
import win32gui
import time
from telebot import types
from handlers.kohelper import KOHelperHandler
from tinydb import TinyDB,Query
import signal
import configparser
import random
import base64
from threading import Thread, Event, Timer
import win32api
import win32con
import pywinauto
from ahk import AHK
import mouse
import interception
import re

interception.auto_capture_devices(keyboard=True, mouse=True)
ahk = AHK()
user32 = ctypes.windll.user32
ScreenSize = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
KO_PATH = "C:\\NTTGame\\KnightOnlineEn\\"
OTP_PATH = "C:\\Program Files (x86)\\AnyOTPSetup\\"
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.FAILSAFE = False


eventThread = False
threadRunning = False
macroRunning = False
macroThread = False
minorThread = False
lightFeetThread = False
attacking = False

priest_heal_timer = False
priest_malice_timer = False
mana_timer = False

userInfoThread = False
health = False
mana = False
isDead = False
found_window = False
otp_pid=0
SUNUCU_POS = {'zero':(645,363),'agartha':(645,335)}
def search_image(image):
        count = imagesearch_count("images/"+image)
        return count
        
def get_text(screenxy: tuple, scale: int, psm: int, whitelist: str = "") -> str:
    """Returns text from screen coordinates"""
    screenshot = ImageGrab.grab(bbox=screenxy)
    resize = image_resize(screenshot, scale)
    array = image_array(resize)
    grayscale = image_grayscale(array)
    thresholding = image_thresholding(grayscale)
    return pytesseract.image_to_string(thresholding,
                                       config=f'--psm {psm} -c tessedit_char_whitelist={whitelist}').strip()
def image_resize(image: int, scale: int) -> Any:
    """Resizes the image using the scale passed in argument two"""
    (width, height) = (image.width * scale, image.height * scale)
    return image.resize((width, height))

def image_array(image: ImageGrab.Image) -> Any:
    """Turns the image into an array"""
    image = np.array(image)
    image = image[..., :3]
    return image

def image_grayscale(image: ImageGrab.Image) -> Any:
    """Converts an image to grayscale so OCR has an easier time deciphering characters"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def image_thresholding(image: ImageGrab.Image) -> Any:
    """Applies thresholding to the image https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html"""
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

def sleep_random():
    time.sleep(random.uniform(0.1, 0.3))

def double_click(coords:tuple)->None:
    pydirectinput.moveTo(coords[0]+2, coords[1]+2)
    pydirectinput.doubleClick()

def left_click(coords: tuple) -> None:
    """Left clicks at argument ones coordinates"""    
    pydirectinput.moveTo(coords[0]+2, coords[1]+2)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()

def left_clickwin32(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep_random() 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    sleep_random()

def left_clickwinauto(x,y):
    pywinauto.mouse.click(button='left', coords=(x, y))

def left_clickpyautogui(x,y):
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')

def left_clickahk(x,y):
    #ahk.mouse_move(x, y, speed=10, relative=True)
    ahk.click(x, y, coord_mode='Screen') 

def left_clickmouse(x,y):
    mouse.press(button='left')
    time.sleep(0.5)
    mouse.move(x, y, absolute=True, duration=0.1)
    time.sleep(0.5)
    mouse.release(button='left')
    mouse.click(button='left')
    mouse.double_click(button='left')

def left_clickinterception(x,y):
    interception.click(x, y, button="left", delay=1)

def press(key)->None:
    pydirectinput.press(key)

def press_and_wait(key,ms)->None:
    pydirectinput.keyDown(key)
    time.sleep(ms)
    pydirectinput.keyUp(key)

def PC_Name():
    return f'{os.environ["COMPUTERNAME"]} - {os.environ["USERNAME"]}'
    
def Uptime():
    pythoncom.CoInitialize()
    wmiob = wmi.WMI()
    sdata = wmiob.Win32_PerfFormattedData_PerfOS_System()
    uptime = sdata[-1].SystemUpTime
    tnow = datetime.datetime.now()
    utime = datetime.timedelta(seconds=int(uptime))
    boot = tnow-utime
    return "{}:{}:{}".format(boot.hour, boot.minute, boot.second)

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % os.environ["USERNAME"]
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'cd %s && python "%s\bot_kontrol.py"' % (file_path,file_path))

def restart_pc():
    subprocess.Popen("shutdown -r -t 1")

def today():
    return  datetime.datetime.today().strftime('%Y-%m-%d')

def CPU_Count():
    return multiprocessing.cpu_count()

def CPU_Usage():
    return  psutil.cpu_percent(0)

def Total_RAM():
    total_ram = psutil.virtual_memory()[0]/1024**3
    return "%.2f GB" % total_ram

def Free_RAM():
    free_ram = psutil.virtual_memory()[4]/1024**3
    return "%.2f GB" % free_ram

def Total_HDD():
    obj_Disk = psutil.disk_usage('/')
    return "%.2f GB" % float(obj_Disk[0]/1024**3)

def Free_HDD():
    obj_Disk = psutil.disk_usage('/')
    return "%.2f GB" % float(obj_Disk[2]/1024**3)

def IP_Address():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def Location():
    ip_address = IP_Address()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return f'{location_data["city"]} / {location_data["country"]}'

def startbot(message):
    if len(message.text.split(" "))>1:
        time.sleep(float(message.text.split(" ")[1])*60)
    print("calıstırılıyor..")
    with interception.hold_key("alt"):
        interception.press("tab")
        pos = imagesearch("./images/knightevolution.png")
        if pos[0]!=-1:
            left_clickinterception(pos[0]+50,pos[1]+50)

def SS1080():
    screenshot = pyautogui.screenshot()
    screenshot.save(r"./tmp.png")
    return './tmp.png'

def OpenLauncher(error:bool=False):
    if(error):
        ret = "--> Giriş başarısız oldu tekrar deneniyor.\r\n"
    else:
        ret = ""
    found_window=False
    if os.path.exists(KO_PATH+"Launcher.exe"):
        os.system("start "+KO_PATH+"Launcher.exe")
        ret = ret + "--> Launcher başlatıldı..\n"
        time.sleep(1)
        launcherbar = search_image("launcherbar.png")
        if launcherbar>0:
            ret = ret + "--> Sunucu erişimi aktif.\n"
        else:
            ret = ret + "--> Sunucu erişimi yok veya patch var.\n"
        startbtn=imagesearch("./images/start.png")
        if startbtn[0]!=-1:
            ret = ret +"--> Oyun başlatıldı. Giriş yapılıyor..\n";
            left_click(startbtn)
        else:
            ret = ret +"--> Start yok. Kontrol edin.\n"
        return ret
    else:
        return "KO_PATH değerini kontrol edin."

def callback(hwnd, extra) -> None:  # pylint: disable=unused-argument
    global found_window
    if "Knight OnLine Client" not in win32gui.GetWindowText(hwnd):
        return
    rect = win32gui.GetWindowRect(hwnd)
    x_pos = rect[0]
    y_pos = rect[1]
    width = rect[2] - x_pos
    height = rect[3] - y_pos
    found_window = True

def getUsernamePassword():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    username = config["ACCOUNT"]["username"]
    password = config["ACCOUNT"]["password"]
    return {"username":username, "password":password}

def getOTPPassword():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config["ACCOUNT"]["otp_pass"]

def LoginKO():
    global found_window
    while not found_window:
        win32gui.EnumWindows(callback, None)
        time.sleep(3)
    time.sleep(3)
    login_screen = False
    while not login_screen:
        pos = imagesearch("./images/loginscreen.png")
        if pos[0]!=-1:
            login_screen = True
    time.sleep(1)
    #left_click(300,300)
    #press("enter")
    creds = getUsernamePassword()
    for i in range(0,len(creds["username"])):
        press(creds["username"][i])
        time.sleep(random.uniform(0.1, 0.3))
    press("tab")
    for i in range(0,len(creds["password"])):
        press(creds["password"][i])
        time.sleep(random.uniform(0.1, 0.3))
    press("enter")
    #press username and tab press password and enter
    ret = "--> Giriş yapıldı. OTP için kod bekleniyor..\r\n"
    text = get_text((530,330,810,350),1,1)
    while not "correct OTP password" in text:
        print(text)
        text = get_text((530,330,810,350),1,1)
        time.sleep(2)
    otp_key = OTPFunc()
    ret = ret + "--> OTP kod alındı : "+otp_key +"\r\n"
    ret = ret + "--> Giriş yapılıyor..\r\n"
    #left_click((10,10))
    time.sleep(2)
    for i in range(0,len(otp_key)):
        key = otp_key[i]
        press(key)
        time.sleep(random.uniform(0.1, 0.3))
    press("enter")
    time.sleep(2)
    text = get_text((530,310,730,330),1,1)
    if "OTP Number is incorrect" in text:
        subprocess.Popen("taskkill /F /IM KnightOnline*")
        time.sleep(3)
        ret = ret + "--> Giriş yapılamadı tekrar deneyin. /login"
    else:
        press("enter")
    ret = ret +"--> Giriş yapıldı. Sunucu seçiniz."
    return ret

def OpenOTP():
    found_window=False
    if os.path.exists(OTP_PATH+"AnyOTP.exe"):
        proc = subprocess.Popen(OTP_PATH+"AnyOTP.exe")
        otp_pid = proc.pid
        #os.system('start "'+OTP_PATH+'AnyOTP.exe"')
        ret = "--> AnyOTP başlatıldı..\n"
        time.sleep(1)
        return ret
    else:
        return "OTP_PATH değerini kontrol edin."

def OTPLogin():
    password = getOTPPassword()
    for i in range(0,len(password)):
        key = password[i]
        pos = imagesearch("./images/"+key+".png")
        if pos[0]!=-1:
            left_click(pos)
            time.sleep(random.uniform(0.1, 0.3))
        else:
            print("otp sifre hatası")
    pos = imagesearch("./images/otp_confirm.png")
    if pos[0]!=-1:
        left_click((pos[0]+2,pos[1]+2))
    else:
        print("otp confirm hatası")

def getOTP():
    ret = 0
    pos = imagesearch("./images/otp_number_title.png")
    if pos[0]!=-1:
        x = pos[0]-100
        y = pos[1]+30
        width = x+370
        height = y+70
        ret = get_text((x,y,width,height),1,1)
    else:
        print("otp number okuma hatası")
    subprocess.Popen("taskkill /F /IM AnyOTP.exe")
    return ret

def OTPFunc():
    OpenOTP()
    OTPLogin()
    return getOTP()

def EnterOTP(otp):
    ret = "--> OTP girişi başarılı.\n"
    ret = ret + "--> Sunucuya giriş yapılıyor.\n"
    ret = ret + "--> Karakter seçimi başarılı.\n"
    ret = ret + "--> Giriş tamamlandı.\n"
    return ret

def SunucuSecim(message,bot):
    sunucu = message.data.split(":")[1]
    left_click(SUNUCU_POS[sunucu])
    btns_arr = {f'{sunucu}1':f'altserver:{sunucu}1',f'{sunucu}2':f'altserver:{sunucu}2',f'{sunucu}3':f'altserver:{sunucu}3',f'{sunucu}4':f'altserver:{sunucu}4',f'{sunucu}5':f'altserver:{sunucu}5',f'{sunucu}6':f'altserver:{sunucu}6'}
    markup = gen_markup(btns_arr)
    bot.send_message(message.message.chat.id,f"<i><b>Alt Sunucu Seçimi:</b></i>\n\n\nLütfen alt sunucu seçin.", reply_markup=markup,parse_mode='html')

def AltSunucuSecim(message,bot):
    text = message.data.split(":")[1]
    sunucu = text[:-1]
    altsunucu = int(text[-1:])
    xmesafe = 190
    ymesafe = (altsunucu-1)*24
    x = SUNUCU_POS[sunucu][0]+xmesafe
    y = SUNUCU_POS[sunucu][1]+ymesafe
    left_click((x,y))
    left_click((x,y))
    time.sleep(2)
    pos = imagesearch("./images/refreshbtn.png")
    if pos[0]!=-1:
        bot.send_message(message.message.chat.id,f"!!! Captcha doğrulaması gerekiyor.\r\nLütfen /ss1080 komutu ile captchaya bakıp /captcha ile cevabı iletin.")
    else:
        bot.send_message(message.message.chat.id,f"Sunucuya giriş başarılı.")
        time.sleep(3)
        bot.send_message(message.message.chat.id,f"{LoginTamamla()}")

def captcha(message,bot):
    captcha = extract_arg(message.text)[0]
    left_click((622,451))
    for i in range(0,len(captcha)):
        if captcha[i].isupper():
            press("capslock")
        press(captcha[i].lower())
        if captcha[i].isupper():
            press("capslock")
        time.sleep(random.uniform(0.1, 0.3))
    press("enter")
    return "Captcha girildi. Sonuç bekleniyor."

def LoginTamamla():
    pos = imagesearch("./images/startgame_btn.png")
    while pos[0]==-1:
        time.sleep(2)
        pos = imagesearch("./images/startgame_btn.png") 
    press("enter")
    time.sleep(5)
    pos = imagesearch("./images/menu_btn.png")
    while pos[0]==-1:
        time.sleep(2)
        pos = imagesearch("./images/menu_btn.png")
    return "<b>Giriş tamamlandı.</b>"

def extract_arg(arg):
    return arg.split()[1:]

def gen_markup(btns_arr):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = len(btns_arr)
    for title,data in btns_arr.items():
        markup.add(types.InlineKeyboardButton(title, callback_data=data))
    return markup

def PartiDCMS(message,bot):
    db_func('step',1)
    ms = int(message.data.split(":")[1])
    db_func('partidcms',ms)
    KOHelperHandler.stepone(message.message,bot)

def OlumMS(message,bot):
    db_func('step',2)    
    ms = int(message.data.split(":")[1])
    db_func('olumms',ms)
    KOHelperHandler.steptwo(message.message,bot)

def DCMS(message,bot):
    db_func('step',3)    
    ms = int(message.data.split(":")[1])
    db_func('dcms',ms)
    KOHelperHandler.stepthree(message.message,bot)

def Nation(message,bot):
    db_func('step',4)    
    nation = int(message.data.split(":")[1])
    db_func('nation',nation)    
    KOHelperHandler.stepfour(message.message,bot)

def WarriorCount(message,bot):
    db_func('step',5)    
    count = int(message.data.split(":")[1])
    db_func('wrcount',count)  
    KOHelperHandler.stepfive(message.message,bot)
    
def RogueCount(message,bot):
    db_func('step',6)    
    count = int(message.data.split(":")[1])
    db_func('rgcount',count) 
    KOHelperHandler.stepsix(message.message,bot)
    
def PriestCount(message,bot):
    db_func('step',7)    
    count = int(message.data.split(":")[1])
    db_func('prcount',count) 
    KOHelperHandler.stepseven(message.message,bot)
    
def MageCount(message,bot):
    db_func('step',8)    
    count = int(message.data.split(":")[1])
    db_func('mgcount',count)
    print("ko helper baslatiliyor.")
    chat_id = message.message.chat.id
    token = bot.token
    start_KOHelper(chat_id,token)
    KOHelperHandler.bot_started(message.message,bot)
    
def start_KOHelper(chat_id,token):    
    partidcms = getValueFromDB('partidcms')["value"]
    olumms = getValueFromDB('olumms')["value"]
    dcms = getValueFromDB('dcms')["value"]
    nation = getValueFromDB('nation')["value"]
    wrcount = getValueFromDB('wrcount')["value"]
    rgcount = getValueFromDB('rgcount')["value"]
    prcount = getValueFromDB('prcount')["value"]
    mgcount = getValueFromDB('mgcount')["value"]
    starter_url = f"python ./kohelper.py --chat_id={chat_id} --token={token} --partidcms={partidcms} --olumms={olumms} --dcms={dcms} --nation={nation} --wrcount={wrcount} --rgcount={rgcount} --prcount={prcount} --mgcount={mgcount}"
    process = subprocess.Popen(starter_url)
    db_func('process',process.pid)

def stop_KOHelper():
    process_id = getValueFromDB('process')["value"]
    os.kill(process_id, signal.SIGTERM)
 
def setJob(message):
    job = message.text.split(" ")[1]
    db_func('job',job)
 
def setNick(message):
    nick = message.text.split(" ")[1]
    db_func('nick',nick)

def setPos(message):
    sira = message.text.split(" ")[1]
    db_func('ptpos',sira)

def addTP(message):
    nick = message.text.split(" ")[1]
    db_func('tplist',nick)

def delTP(message):
    nick = message.text.split(" ")[1]
    db_func('tplist',"")

class EventThread(Thread):
    def __init__(self, *args, **kwargs):
        super(EventThread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.waitForSec = 600
    
    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def check_death(self):
        #print("check death")
        confirm_btn =  imagesearch("./images/confirm_btn.png")
        #print(confirm_btn)
        if confirm_btn[0]!=-1:
            left_clickinterception(confirm_btn[0]+10,confirm_btn[1]+10)
    def run(self):
        while not self.stopped():
            self.check_death()
            time.sleep(2)
            warprejoin_pos = imagesearch("./images/10xwarpre.png")
            warpre1x_pos =  imagesearch("./images/1xwarpre.png")
            if ((warprejoin_pos[0]!=-1) or (warpre1x_pos[0]!=-1)):
                old_pos = mouse.get_position()
                if (warpre1x_pos[0]!=-1):
                    pos = warpre1x_pos
                else:
                    pos = warprejoin_pos
                print(f"Hedef bulundu. Basılıyor..")
                #bot.send_message(message.message.chat.id,f"/warprejoin Hedef bulundu. Basılıyor...")
                x = int(pos[0])-14
                y = int(pos[1])+84
                left_clickmouse(x,y)
                left_clickinterception(x,y)
                interception.move_to(old_pos[0], old_pos[1])
            print(f"{self.waitForSec} saniye bekleniyor..")
            time.sleep(self.waitForSec)

def warprejoin(message):
    global threadRunning
    global eventThread
    
    if len(message.text.split(" "))>1:
        ret = "islem durduruldu\r\n"
        eventThread.stop()
        threadRunning = False
    else:
        if threadRunning == True:
            ret = "islem zaten calisiyor..\r\n"
        else:
            ret = "islem baslatildi..\r\n"
            eventThread = EventThread()
            eventThread.start()
            threadRunning = True
    return ret


class UserInfoThread(Thread):
    def __init__(self, *args, **kwargs):
        super(UserInfoThread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.count = 0
    
    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()
    
    def health_check(self):
        try:
            text = get_text((90,35,180,50),1,1)
            text = text.split("/")
            text[0] = re.sub('\D','',text[0])
            text[1] = re.sub('\D','',text[1])
            #print(f"{text[0]} : {text[1]}")
            if int(text[0]) + 60 > int(text[1]):
                return True
            else:
                return False
        except:
            return False
    
    def mana_check(self):
        try:
            text = get_text((90,50,175,65),1,1)
            text = text.split("/")
            text[0] = re.sub('\D','',text[0])
            text[1]=re.sub('\D','',text[1])
            if int(text[0]) + 1920 > int(text[1]):
                return True
            else:
                return False
        except:
            return False
    
    def check_death(self):
        #print("check death")
        confirm_btn =  imagesearch("./images/confirm_btn.png")
        #print(confirm_btn)
        if confirm_btn[0]!=-1:
            return True
        else:
            return False
    
    def awake(self):
        left_clickinterception(confirm_btn[0]+10,confirm_btn[1]+10)
    
    def run(self):
        global health
        global mana
        global isDead
        while not self.stopped():
            #health = self.health_check()
            #mana = self.mana_check()
            isDead = self.check_death()
            if isDead:
                macroRunning=False
            #print(f"hp -> {health} mana -> {mana}")

class NewMacroTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    
    def stop(self):
        self._timer.cancel()
        self.is_running = False
        
class MacroThread(Thread):
    import time
    global attacking
    def __init__(self, *args, **kwargs):
        super(MacroThread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.count = 0
    
    def stop(self):
        self._stopper.set()
        macroRunning = False

    def stopped(self):
        return self._stopper.isSet()
    
    def press_hold_and_key(self,hold,key):
        with interception.hold_key(hold):
            interception.press(key,interval=0.0001)
    
    def press(self,key):
        interception.press(key,interval=0.0001)
    
    def roguebow(self):
        #if keyboard.read_key() == "end":
        #    self.stop()
        #start = time.perf_counter()
        self.press("z")
        #attacking = True
        self.press("3")
        #attacking = False
        time.sleep(0.5)
        #attacking = True
        self.press("w")
        self.press("4")
        time.sleep(0.5)
        self.press("w")
        #time.sleep(1)
        #attacking = False
        #end = time.perf_counter()
        #print("geçen süre : ", (end-start))
    
    def run(self):
        while not self.stopped():
            self.roguebow()

class MinorThread(Thread):
    import time
    def __init__(self, *args, **kwargs):
        super(MinorThread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.count = 0
    
    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()
    
    def press_hold_and_key(self,hold,key):
        with interception.hold_key(hold):
            interception.press(key,interval=0.0001)
    
    def minor_combo(self):
        interception.key_down("ctrl")
        interception.press(key="0", presses=25, interval=0.001)
        interception.key_up("ctrl")
    
    def press(self,key):
        interception.press(key,interval=0.0001)
    
    def run(self):
        global attacking
        global health
        global mana
        while not self.stopped():
            #if keyboard.read_key() == "end":
            #    self.stop()
            if not health:
                self.minor_combo()
            if not mana : 
                self.press("9")

class LightFeetThread(Thread):
    import time
    def __init__(self, *args, **kwargs):
        super(LightFeetThread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.count = 0
    
    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()
    
    def press_hold_and_key(self,hold,key):
        with interception.hold_key(hold):
            interception.press(key)
    
    def press(self,key):
        interception.press(key)
    
    def run(self):
        while not self.stopped():
            if self.count>6 or self.count==0:
                self.press("2")
                self.press("2")
                self.press("2")
                if self.count>6:
                    self.count = 0
            else:
                time.sleep(1)
            self.count = self.count + 1

def roguemacro(message):
    global macroRunning
    global macroThread
    global minorThread
    global userInfoThread
    global lightFeetThread
    ret = ""
    if len(message.text.split(" "))>1:
        ret = "islem durduruldu\r\n"
        macroThread.stop()
        minorThread.stop()
        userInfoThread.stop()
        lightFeetThread.stop()
        macroRunning = False
    else:
        if macroRunning == True:
            ret = "makro zaten calisiyor..\r\n"
        else:
            ret = "islem baslatildi..\r\n"
            userInfoThread = UserInfoThread()
            userInfoThread.start()
            macroThread = MacroThread()
            macroThread.start()
            minorThread = MinorThread()
            minorThread.start()
            lightFeetThread = LightFeetThread()
            lightFeetThread.start()
            macroRunning = True
    return ret

def xpriestmacro(message):
    global macroRunning
    global macroThread
    global userInfoThread
    ret = ""
    if len(message.text.split(" "))>1:
        ret = "islem durduruldu\r\n"
        macroThread.stop()
        #userInfoThread.stop()
        macroRunning = False
    else:
        if macroRunning == True:
            ret = "makro zaten calisiyor..\r\n"
        else:
            ret = "islem baslatildi..\r\n"
            #userInfoThread = UserInfoThread()
            #userInfoThread.start()
            macroThread = MacroThread(args='priest')
            macroThread.start()
            macroRunning = True
    return ret

def priestmacro(message):
    global macroRunning
    global priest_heal_timer
    global priest_malice_timer
    global mana_timer
    global userInfoThread
    ret = ""
    if len(message.text.split(" "))>1:
        ret = "islem durduruldu\r\n"
        priest_heal_timer.stop()
        priest_malice_timer.stop()
        mana_timer.stop()
        #userInfoThread.stop()
        macroRunning = False
    else:
        if macroRunning == True:
            ret = "makro zaten calisiyor..\r\n"
        else:
            ret = "islem baslatildi..\r\n"
            #userInfoThread = UserInfoThread()
            #userInfoThread.start()
            priest_heal_timer = NewMacroTimer(5.5,priest_heal,"key")
            priest_heal_timer.start()
            priest_malice_timer = NewMacroTimer(8.9,priest_malice,"key")
            priest_malice_timer.start()
            mana_timer = NewMacroTimer(12,priest_mana,"key")
            mana_timer.start()
            macroRunning = True
    return ret

def priest_heal(key):
    interception.press("3")
    time.sleep(1)
    
def priest_malice(key):
    interception.press("z")
    interception.press("z")
    interception.press("z")
    interception.press("8")

def priest_mana(key):
    interception.press("0")

def TP(message):
    ret = ""
    sira = message.text.split(" ")[1]
    val = getValueFromDB('tplist')["value"]
    if sira == val:
        genie_pos = imagesearch("./images/knightgenie.png")
        if (genie_pos[0]!=-1):
            ret = ret + "Genie durduruluyor.\r\n"
            x = int(genie_pos[0])+115
            y = int(genie_pos[1])+9
            left_click((x,y))
        pos = imagesearch("./images/ptclose.png")
        y = pos[1]
        new_y = (int(sira)-1)*55 + int(y) + 33
        new_pos = (int(pos[0]) - 17,new_y)
        left_click(new_pos)
        left_click(new_pos)
        press("f3")
        press("1")
        time.sleep(2)
        if (genie_pos[0]!=-1):
            x = int(genie_pos[0])+88
            y = int(genie_pos[1])+8
            left_click((x,y))
        ret = ret + "TP işlemi tamamlandı. \r\n"
    else:
        ret = "error"
    return ret

def shout(message):
    mesaj = message.text.split(" ")
    if(len(mesaj)<=1):
        process_id = getValueFromDB('shout_proc')["value"]
        os.kill(process_id, signal.SIGTERM)
        return "Eylem durduruldu."
    else:
        new_msg = ""
        for i in mesaj[1:]:
            new_msg += i+" "
        msg_bytes = new_msg.encode('ascii')
        base64_bytes = base64.b64encode(msg_bytes)
        base64_message = base64_bytes.decode('ascii')
        client = base64.b64encode(("Knight Evolution").encode('ascii')).decode('ascii')
        starter_url = f"python ./shout.py --client='{client}' --message={base64_message} --interception=True"
        process = subprocess.Popen(starter_url)
        db_func('shout_proc',process.pid)
        return "Eylem başlatıldı. İptal etmek için sadece /shout atınız."

def call_tp(bot,channel_id):
    sira = getValueFromDB("ptpos")
    bot.send_message(channel_id,f"/tp {sira}")

def RepairAndSell(message,bot):
    status = message.data.split(":")[1]
    db_func("repairandsell",status)
    if status == "active":
        RepairAndSellHandler.VIPBag(message.message,bot)
def VIPBag(message,bot):
    vipbag = message.data.split(":")[1]
    db_func("vipbag",vipbag)
    chat_id = message.message.chat.id
    token = bot.token
    start_RepairAndSell(chat_id,token,vipbag)

def start_RepairAndSell(chat_id,token,vipbag):    
    starter_url = f"python ./repairandsell.py --chat_id={chat_id} --token={token} --vipbag={vipbag}"
    process = subprocess.Popen(starter_url)
    db_func('rsprocess',process.pid)

def stop_RepairAndSell():
    process_id = getValueFromDB('rsprocess')["value"]
    os.kill(process_id, signal.SIGTERM)
 

def db_func(key,val):
    if os.path.exists('./kohelper.json'):
        if getValueFromDB(key)!=None:
            update_value_from_db(key,val)
        else:
            insert_to_db(key,val)
    else:
        f= open("./kohelper.json","a+")
        f.write("")
        f.close()
        if getValueFromDB(key)!=None:
            update_value_from_db(key,val)
        else:
            insert_to_db(key,val)

def insert_to_db(key,val):
    db = TinyDB('./kohelper.json')
    db.insert({'name': key, 'value': val})

def update_value_from_db(key,val):
    db = TinyDB('./kohelper.json')
    db.update({'value': val}, Query().name == key)

def getValueFromDB(key):
    db = TinyDB('./kohelper.json')
    result = db.get(Query()['name'] == key)
    return result