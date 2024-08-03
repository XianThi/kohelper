import pyautogui
import time
import math

# Karakterin yönünü hesaplayan fonksiyon
def calculate_direction(start_x, start_y, target_x, target_y):
    angle = math.atan2(target_y - start_y, target_x - start_x) * 180 / math.pi
    if angle < 0:
        angle += 360
    return angle

# press_and_wait fonksiyonunu tanımlayın
def press_and_wait(key, ms):
    pyautogui.keyDown(key)
    time.sleep(ms)
    pyautogui.keyUp(key)

    
# Pyautogui'yi varsayılan ayarlarla başlatın
pyautogui.FAILSAFE = True

def move_to_target(target_x, target_y):
    walk_speed = 2.7
    rotation_speed = 5.87

    while True:
        current_x, current_y = getCurrentCoords()

        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        if distance <= 1:
            break

        direction = calculate_direction(current_x, current_y, target_x, target_y)

        if direction > 180:
            press_and_wait('a', rotation_speed / 180 * (direction - 180))
        else:
            press_and_wait('d', rotation_speed / 180 * direction)

        steps_x = 7 / math.sqrt(2)
        steps_y = 7 / math.sqrt(2)

        press_and_wait('w', walk_speed * steps_x)

        time.sleep(1)

        new_x, new_y = getCurrentCoords()
        new_distance = math.sqrt((target_x - new_x)**2 + (target_y - new_y)**2)

        if new_distance >= distance:
            continue

        if new_x - current_x > 0 and new_y - current_y > 0:
            press_and_wait('d', rotation_speed / 180 * (direction - 180))
        elif new_x - current_x > 0 and new_y - current_y < 0:
            press_and_wait('a', rotation_speed / 180 * direction)
        elif new_x - current_x < 0 and new_y - current_y > 0:
            press_and_wait('d', rotation_speed / 180 * direction)
        elif new_x - current_x < 0 and new_y - current_y < 0:
            press_and_wait('a', rotation_speed / 180 * (direction - 180))

        time.sleep(5)

    while True:
        current_x, current_y = getCurrentCoords()
        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        if distance < 1:
            break
        press_and_wait('w', walk_speed)

    print("Hedefe ulaşıldı.")
