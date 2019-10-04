import low_level_keyboard_hook as keyboard
from ctypes import c_short, windll
import ctypes
from win32con import *
from nightlight import *
import nightlight
import win32gui
import time
from threading import Thread
import queue
import pyautogui
import atexit

# -------------------------------------------------------------------
# functions to control nightlight

settings_window = None
slider_position = 50
mouse_position = None


def open_window():
    global settings_window
    if settings_window is None:
        settings_window = open_night_light()
        time.sleep(0.3)


def close_window():
    global settings_window
    if settings_window:
        nightlight.close_night_light()
        settings_window = None
    restaure_mouse_position()


def increase_nightlight():
    open_window()
    save_mouse_position()
    move_cursor(5)


def decrease_nightlight():
    open_window()
    save_mouse_position()
    move_cursor(-5)


def save_mouse_position():
    global mouse_position
    if not mouse_position:
        mouse_position = pyautogui.position()


def restaure_mouse_position():
    global mouse_position
    if mouse_position:
        pyautogui.moveTo(mouse_position)
        mouse_position = None

# -------------------------------------------------------------------
# a worker thread and its tasks queue to execute nightlight actions

tasks = queue.Queue()

def next_task():
    while True:
        fun = tasks.get()
        fun()
        tasks.task_done()

t = Thread(target=next_task)
t.daemon = True
t.start()

# -------------------------------------------------------------------
# the keyboard hooked callback to create the hotkeys

ctrl_down = False

def event_handler(wParam, kb):
    global ctrl_down

    if kb.vkCode in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
        ctrl_down = (wParam == WM_KEYDOWN)
        if wParam == WM_KEYUP:
            tasks.put(close_window)

    elif ctrl_down and kb.vkCode in (VK_VOLUME_DOWN, VK_VOLUME_MUTE, VK_VOLUME_UP):
        if wParam == WM_KEYDOWN:
            if kb.vkCode == VK_VOLUME_DOWN:
                tasks.put(decrease_nightlight)
            elif kb.vkCode == VK_VOLUME_UP:
                tasks.put(increase_nightlight)
        return True  # True means we don't propagate the message further

# -------------------------------------------------------------------

def main():
    keyboard.add_listener(event_handler)
    keyboard.listen()
    
if __name__=='__main__':
    main()