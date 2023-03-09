import pyautogui
import time
import math

# Hedef koordinatlarını buraya girin
target_x = 100
target_y = 200

# Karakterin yönünü hesaplayan fonksiyon
def calculate_direction(start_x, start_y, target_x, target_y):
    angle = math.atan2(target_y - start_y, target_x - start_x) * 180 / math.pi
    if angle < 0:
        angle += 360
    return angle

# Pyautogui'yi varsayılan ayarlarla başlatın
pyautogui.FAILSAFE = True

# Hedefe ulaşana kadar hareket edin
while True:
    # Mevcut koordinatları alın
    current_x, current_y = getCurrentCoords()

    # Karakterin yönünü hesaplayın
    direction = calculate_direction(current_x, current_y, target_x, target_y)

    # Yöne göre karakteri döndürün
    if direction > 180:
        pyautogui.press('a')
    else:
        pyautogui.press('d')

    # Adımları 45 derecelik açıya göre hesaplayın
    steps_x = 7 / math.sqrt(2)
    steps_y = 7 / math.sqrt(2)

    # Hedefe doğru ilerleyin
    pyautogui.press('w')
    time.sleep(1)

    # Hedefe doğru ilerleyip ilerlemediğimizi kontrol edin
    new_x, new_y = getCurrentCoords()
    distance = math.sqrt((new_x - target_x)**2 + (new_y - target_y)**2)

    if distance < 10:
        break

    # Hedefe doğru hareket ederken sapma olursa karakteri yeniden hedefe yöneltin
    if new_x - current_x > 0 and new_y - current_y > 0:
        pyautogui.press('d')
    elif new_x - current_x > 0 and new_y - current_y < 0:
        pyautogui.press('a')
    elif new_x - current_x < 0 and new_y - current_y > 0:
        pyautogui.press('d')
    elif new_x - current_x < 0 and new_y - current_y < 0:
        pyautogui.press('a')

    # 5 saniye bekleyin ve yeniden hareket etmeye başlayın
    time.sleep(5)

# Hedefin 1 birim yarıçapında durun
while True:
    current_x, current_y = getCurrentCoords()
    distance = math.sqrt((current_x - target_x)**2 + (current_y - target_y)**2)
    if distance < 1:
        break
    time.sleep(1)

# Programı sonlandırın
print("Hedefe ulaşıldı.")
