"""Module to register a LowLevelKeyBoardHook to listen to keyboard events in Windows.

Call the function `add_listener(callback)` to register a listener. Then call the function `listen()`,
or run your own GetMessage/TranslateMessage/DispatchMessage loop.

The callback has this signature: `(wParam, lParam) -> Bool`.
- `wParam` can be any of `win32con.{WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP}`
- `lParam` is a struct whose member of interest is `lParam.vkCode`. It can be any of `win32con.VK_*`
- Return True if you want to intercept to keyboard event and None or False if you want to let it propagate.

Last modified: October 2019
Author: Julien Harbulot
"""

from collections import namedtuple
import atexit
import ctypes
from ctypes.wintypes import DWORD
from ctypes import windll, wintypes, Structure, WINFUNCTYPE, c_int, byref
from win32con import WH_KEYBOARD_LL

user32 = windll.user32
kernel32 = windll.kernel32

# --------------------------------------------------------------------------------------------
# Define some types to use with C functions

class KBDLLHOOKSTRUCT(Structure): 
    _fields_ = [
        ('vkCode',      DWORD),
        ('scanCode',    DWORD),
        ('flags',       DWORD),
        ('time',        DWORD),
        ('dwExtraInfo', DWORD)
    ]

kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
user32.SetWindowsHookExA.argtypes = (c_int, wintypes.HANDLE, wintypes.HMODULE, wintypes.DWORD)
user32.CallNextHookEx.argtypes = (wintypes.HHOOK, c_int, wintypes.WPARAM, wintypes.LPARAM)
user32.CallNextHookEx.restype = wintypes.LPARAM
HOOKPROC = WINFUNCTYPE(wintypes.LPARAM, c_int, wintypes.WPARAM, wintypes.LPARAM)

# --------------------------------------------------------------------------------------------
# We must ensure pointers to callbacks are not garbage collected, so I'm having them as globals
# See: https://docs.python.org/2/library/ctypes.html#callback-functions

pointers = [] 
"""Keeps all the pointers sent to c_types to prevent them from being garbage collected."""

# --------------------------------------------------------------------------------------------
# see: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexa

def add_listener(event_handler):
    """Adds a WH_KEYBOARD_LL hook which redirect wParam and lParam to the provided `event_handler`.
    
    It's better to call this function only once and handle your listeners yourself.
    """

    # see: https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644985(v=vs.85)
    def low_level_handler(nCode, wParam, lParam):
        """The handler sent to ctypes, it forwards wParam and lParam to the `event_handler`."""

        if nCode >= 0:  # per the documentation: when nCode < 0, forward message without further processing
            kb = KBDLLHOOKSTRUCT.from_address(lParam)
            if event_handler(wParam, kb):
                return 1  # do not propagate message
        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    pointer = HOOKPROC(low_level_handler)
    pointers.append(pointer)  # save pointer to make sure it's not garbage collected!
    hook_id = user32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW(None), DWORD(0))
    atexit.register(user32.UnhookWindowsHookEx, hook_id)  # register to remove the hook when the interpreter exits.
    
# --------------------------------------------------------------------------------------------

def listen():
    """Runs a usual Windows loop: GetMessage/TranslateMessage/DispatchMessage."""

    msg = msg = wintypes.MSG()
    while True:
        user32.GetMessageA(byref(msg), 0, 0, 0)
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageW(byref(msg))

# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    add_listener(print)
    listen()
