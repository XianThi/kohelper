import random
import pydirectinput
import time

def left_click(coords: tuple) -> None:
    """Left clicks at argument ones coordinates"""    
    pydirectinput.moveTo(coords[0]+2, coords[1]+2)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()

def left_click_and_wait(coords:tuple,ms):
    pydirectinput.moveTo(coords[0], coords[1])
    pydirectinput.mouseDown()
    time.sleep(ms)
    pydirectinput.mouseUp()

def left_click_from_to(from_coords: tuple, to_coords:tuple)->None:
    pydirectinput.moveTo(from_coords[0],from_coords[1])
    pydirectinput.mouseDown()
    pydirectinput.moveTo(to_coords[0],to_coords[1])
    pydirectinput.mouseUp()

def right_click(coords: tuple) -> None:
    """Right clicks at argument ones coordinates"""
    pydirectinput.moveTo(coords[0]+2, coords[1]+2)
    pydirectinput.mouseDown(button="right")
    pydirectinput.mouseUp(button="right")
def right_click_drag_drop(start_pos: tuple,stop_pos:tuple) -> None:
    """Right clicks at argument ones coordinates"""
    pydirectinput.moveTo(start_pos[0], start_pos[1])
    pydirectinput.mouseDown(button="right")
    pydirectinput.moveTo(stop_pos[0],stop_pos[1])
    pydirectinput.mouseUp(button="right")

def move_mouse(coords: tuple) -> None:
    """Moves mouse to argument ones coordinates"""
    pydirectinput.moveTo(coords[0], coords[1])

def move_mouse_toitem(coords: tuple)->None:
    pydirectinput.moveTo(coords[0]+3,coords[1]+3)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()

def move_mouse_and_wait(coords: tuple,ms) -> None:
    """Moves mouse to argument ones coordinates"""
    pydirectinput.moveTo(coords[0], coords[1])
    time.sleep(ms)
    
def press(key)->None:
    pydirectinput.press(key)

def press_and_wait(key,ms)->None:
    pydirectinput.keyDown(key)
    time.sleep(ms)
    pydirectinput.keyUp(key)

def press_two_key_and_wait(key,keyx,ms)->None:
    pydirectinput.keyDown(key)
    pydirectinput.keyDown(keyx)
    time.sleep(ms)
    pydirectinput.keyUp(key)
    pydirectinput.keyUp(keyx)