import os
import datetime
import wmi
import multiprocessing
import psutil
import requests
import pyautogui
import base64

def PC_Name():
    return f'{os.environ["COMPUTERNAME"]} - {os.environ["USERNAME"]}'
    
def Uptime():
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