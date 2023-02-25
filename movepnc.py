from sympy import *
import math
import mk_functions
import time
import ocr
import numpy as np

CURRENT_COORD = [98,73,156,90]

def getCurrentCoords():
    ret = ocr.get_text(CURRENT_COORD,1,1,whitelist=ocr.COORD_WHITELIST)
    #print("current coords : " + ret)
    if len(ret.split(","))>1:
        return ret.split(",")
    else:
        return ret.split(".")

def moveToNPC(current_coords,npc_coords)->bool:
    a,b = symbols('a,b')
    res = 0
    saga = False
    sola = False
    ileri = False
    geri = False
    curr_pos = current_coords
    dst_pos = npc_coords
    x1,y1 = curr_pos
    x2,y2 = dst_pos
    asilx1 = round(x1 * math.sqrt(2))
    asily1 = round(y1 * math.sqrt(2))
    asilx2 = round(x2 * math.sqrt(2))
    asily2 = round(y2 * math.sqrt(2))
    print(asilx1,asily1,asilx2,asily2)
    x_diff = asilx1-asilx2
    y_diff = asily1-asily2
    if x_diff > 0: #x değerini azaltmaya çalışıyoruz.
        geri = False
        ileri = True
    else: #x değerini arttırmaya calısıyoruz
        geri = True
        ileri = False
    if y_diff >0: # y değerini azaltmaya calısıyoruz.
        saga = False  
        sola = True 
    else: # y değerini arttırmaya calısıyoruz
        saga = True #
        sola = False

    adima= float(abs(x_diff)*(float(float(math.sqrt(2))/2)))
    adimb= float(abs(y_diff)*(float(float(math.sqrt(2))/2)))
    #adimb = float(abs(y_diff))
    msa =float(adima/1.7)
    msb =float(adimb/1.7)
    print(ileri,geri,saga,sola,adima,adimb,msa,msb)
    if ileri: #x değeri düşürülüyor.
        mk_functions.press_and_wait("d",2.9)
        mk_functions.press_and_wait("w",msa)
        mk_functions.press_and_wait("a",2.9)
    else: #x değeri arttırılıyor.
        #mk_functions.press_and_wait("s",msa*3.3357)
        mk_functions.press_and_wait("w",msa)
    if saga:
        mk_functions.press_and_wait("d",1.45)
        mk_functions.press_and_wait("w",msb)
        mk_functions.press_and_wait("a",1.45)
        
    if sola:
        mk_functions.press_and_wait("a",1.45)
        mk_functions.press_and_wait("w",msb)
        mk_functions.press_and_wait("d",1.45)
    
    return True

time.sleep(2)
#moveToNPC((444,1632),(474,1616)) 
#moveToNPC((446,1619),(531,1558)) 
#mk_functions.press_and_wait("d",0.725)
#mk_functions.press_and_wait("w",10)
#exit()

PATH = [
(454,1622),
(466,1614),
(477,1612),
(514,1571),
(556,1599),
(595,1642),
(605,1649),
]
yurume = 1.7
kosma = 2.7
hiz = kosma
for hedef in PATH:
    pos = getCurrentCoords()
    pos = np.array([int(pos[0]),int(pos[1])])
    hedef = np.array([hedef[0],hedef[1]])
    print(f"hedef : {hedef}")
    while not pos[0]==hedef[0]:
        mk_functions.press_and_wait("w",1/hiz)
        cur_pos = getCurrentCoords()
        second_pos = np.array([int(cur_pos[0]),int(cur_pos[1])])
        ba = pos - second_pos
        bc = hedef - second_pos
        #print(f"ba : {ba} , bc :{bc}")
        if ba[0]==0 & ba[1]==0:
            gerekli_sure=5.87/4
            mk_functions.press_and_wait("a",gerekli_sure)
            continue
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        aranan_aci = 180 - np.degrees(angle)
        gerekli_sure = aranan_aci*5.87/360
        if math.isnan(gerekli_sure):
            gerekli_sure=5.87/4
            mk_functions.press_and_wait("a",gerekli_sure)
            continue
        if hedef[1]>second_pos[1]:
            mk_functions.press_and_wait("a",gerekli_sure)
        else:
            mk_functions.press_and_wait("d",gerekli_sure)
        dist = math.hypot(hedef[0]-second_pos[0], hedef[1]-second_pos[1])
        sure = dist/(hiz*2)
        #print(f"mesafe : {dist} , süre : {sure}")
        mk_functions.press_and_wait("w",sure)
        cur_pos = getCurrentCoords()
        pos = np.array([int(cur_pos[0]),int(cur_pos[1])])