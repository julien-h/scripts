import subprocess
from contextlib import contextmanager
from winrt.windows.system import Launcher
from winrt.windows.foundation import Uri
import pyautogui
import win32gui
import win32con    
import time
import asyncio

_cursor_position = 50

def _cursor_coordinates(pos):
    x_0, y_0 = 2245, 715
    slider_length = 1100
    target_x = x_0 + (pos/100.) * slider_length
    return target_x, y_0


def move_cursor(step):
    global _cursor_position
    _cursor_position = max(0, min(100, _cursor_position + step))
    pyautogui.click(_cursor_coordinates(_cursor_position))
    

async def launch_uri(uri):
    await Launcher.launch_uri_async(Uri(uri))


def open_night_light():
    asyncio.run(launch_uri('ms-settings:nightlight'))
    settings = win32gui.FindWindow(None, 'settings')
    assert settings, "Unable to find settings window..."
    try:
        win32gui.SetForegroundWindow(settings)
    except:
        while win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower() != 'settings':
            pyautogui.hotkey('alt', 'shift', 'tab')
    placement = (0, 1, (-1, -1), (-1, -1), (2187, 0, 3857, 2136))#
    if win32gui.GetWindowPlacement(settings) != placement:
        win32gui.SetWindowPlacement(settings, placement)
    return settings


def close_night_light():
    pyautogui.click(3770, 35)


@contextmanager
def settings_window(sleep_time=0.3):
    settings = open_night_light()
    try:
        if sleep_time:
            time.sleep(sleep_time)
        yield settings
    finally:
        close_night_light()
        #win32gui.PostMessage(settings,win32con.WM_DESTROY,0,0)
        #win32gui.CloseWindow(settings)