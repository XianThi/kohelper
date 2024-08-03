import pydirectinput
import threading
import time

ts_time = 3600
def press_and_wait(key,ms)->None:
    pydirectinput.keyDown(key)
    time.sleep(ms)
    pydirectinput.keyUp(key)

def _input(message, input_type=str):
	while True:
		try:
			return input_type (input(message))
		except:
			pass
				
def ts_bas(key)->None:
    press_and_wait(key,1)
    press_and_wait("down",1)
    
if __name__ == "__main__":
    tskalan = _input("TSnin kalan süresi (dk)?\r\n",int)
    tskey = _input("TSnin skillbar sırası?\r\n",int)
    print(f"{tskalan*60} saniye bekleniyor")
    time.sleep(tskalan*60)
    threading.Thread(target=ts_bas, args=(tskey,), daemon=True)