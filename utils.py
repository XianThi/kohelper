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
user32 = ctypes.windll.user32
ScreenSize = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
KO_PATH = "C:\\NTTGame\\KnightOnlineEn\\"
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

found_window = False
partidcms:int = 0

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


def left_click(coords: tuple) -> None:
    """Left clicks at argument ones coordinates"""    
    pydirectinput.moveTo(coords[0]+2, coords[1]+2)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()

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

def SS1080():
    screenshot = pyautogui.screenshot()
    screenshot.save(r"./tmp.png")
    return './tmp.png'

def OpenLauncher():
    found_window=False
    if os.path.exists(KO_PATH+"Launcher.exe"):
        os.system("start "+KO_PATH+"Launcher.exe")
        ret = "--> Launcher başlatıldı..\n"
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
    left_click((int(width/2),int(height/2)))
    found_window = True
        
def LoginKO(username,password):
    global found_window
    while not found_window:
        win32gui.EnumWindows(callback, None)
        time.sleep(3)
    time.sleep(3)
    login_screen = False
    #while not login_screen:
    #    pos = imagesearch("loginscreen.png")
    #    if pos[0]!=-1:
    #        login_screen = True
    # press username and tab press password and enter
    ret = "--> Giriş yapıldı. OTP için kod bekleniyor.."
    return ret

def EnterOTP(otp):
    ret = "--> OTP girişi başarılı.\n"
    ret = ret + "--> Sunucuya giriş yapılıyor.\n"
    ret = ret + "--> Karakter seçimi başarılı.\n"
    ret = ret + "--> Giriş tamamlandı.\n"
    return ret

def ZeroSunucu(message,bot):
    print("zero seçildi.")

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
 
def db_func(key,val):
    if os.path.exists('./kohelper.json'):
        if getValueFromDB(key)!=None:
            update_value_from_db(key,val)
        else:
            insert_to_db(key,val)
    else:
        f= open("./kohelper.json","w+")
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