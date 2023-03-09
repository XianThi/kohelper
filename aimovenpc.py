import math
import time
import pyautogui

# Karakterin bulunduğu koordinatlar
x1 = 454
y1 = 1622

# Hedef koordinatlar
x2 = 605
y2 = 1649

# İki nokta arasındaki mesafeyi hesapla
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Hedefe doğru yönelmek için gerekli açıyı hesapla
angle = math.atan2(y2 - y1, x2 - x1)
angle = math.degrees(angle)

# Karakterin şu anki yönünü tutan değişken
current_angle = 0

# Döndüğü açıyı hesaplamak için geçen süre
turn_time = 0

# Birim zamanda ilerlenen mesafe
velocity = 2.7  # birim/saniye

# Hedefe varana kadar döngüyü çalıştır
while distance > 0:

    # Eğer yön yanlışsa saat yönünde dön
    if abs(current_angle - angle) > 5:
        pyautogui.keyDown('d')
        time.sleep(0.1)
        pyautogui.keyUp('d')
        current_angle += 72
        turn_time += 1
        if turn_time > 5.87:
            print("Error: Could not adjust direction.")
            break

    # Yön doğruysa ilerle
    else:
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyUp('w')
        distance -= velocity
        x1 += math.cos(math.radians(current_angle)) * velocity
        y1 += math.sin(math.radians(current_angle)) * velocity

print("Distance to destination:", distance)
