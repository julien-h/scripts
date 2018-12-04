"""
Set current process's priority to one of IDLE, BELOW_NORMAL, NORMAL,
ABOVE_NORMAL, HIGH and REALTIME.

This should be cross-platform. On windows this requires the psutil library,
on linux no external libraries. The behavior is slighly different on windows
and linux, as the priority levels are not the same: linux is restricted to
"nice" values between -20 and 19 and in particular, REALTIME is not possible
on linux. The functions thus issues a warning on stderr.

Relevant documentation:
- psutil:         https://psutil.readthedocs.io/en/latest/#psutil.Process.nice
- os.setpriority: https://docs.python.org/3/library/os.html#os.setpriority
"""

import sys
import os

win32 = (sys.platform == 'win32')

if win32:
    import psutil


IDLE         = psutil.IDLE_PRIORITY_CLASS if win32 else 19
BELOW_NORMAL = psutil.BELOW_NORMAL_PRIORITY_CLASS if win32 else 10
NORMAL       = psutil.NORMAL_PRIORITY_CLASS if win32 else 0
ABOVE_NORMAL = psutil.ABOVE_NORMAL_PRIORITY_CLASS if win32 else -10
HIGH         = psutil.HIGH_PRIORITY_CLASS if win32 else -20
REALTIME     = psutil.REALTIME_PRIORITY_CLASS if win32 else -20


def get():
    if win32:
        p = psutil.Process()
        return {
            IDLE:         'IDLE',
            BELOW_NORMAL: 'BELOW_NORMAL',
            NORMAL:       'NORMAL',
            ABOVE_NORMAL: 'ABOVE_NORMAL',
            HIGH:         'HIGH',
            REALTIME:     'REALTIME'
        }.get(p.nice(), p.nice())
    else:
        return os.getpriority(os.PRIO_PROCESS, os.getpid())


def set_priority(LEVEL):
    if win32:
        process = psutil.Process()
        return process.nice(LEVEL)
    else:
        return os.setpriority(os.PRIO_PROCESS, os.getpid(), LEVEL)


def set_idle():
    set_priority(IDLE)


def set_below_normal():
    set_priority(BELOW_NORMAL)


def set_normal():
    set_priority(NORMAL)


def set_above_normal():
    set_priority(ABOVE_NORMAL)


def set_high():
    set_priority(HIGH)


def set_realtime():
    if win32:
        set_priority(REALTIME)
    else:
        print("Warning: REALTIME priority only available"
              " on windows, using HIGH instead", file=sys.stderr)
        set_priority(HIGH)


if __name__ == '__main__':
    from time import sleep

    print('Going to test the priority functions.')
    print('Open your task manager and look at the priority of this process.')
    input("Type any letter when you're ready: ")

    to_test = {
        'idle': set_idle,
        'below normal': set_below_normal,
        'normal': set_normal,
        'above normal': set_above_normal,
        'high': set_high,
        'real time': set_realtime,
    }

    seconds_to_sleep = 5
    for (name, fun) in to_test.items():
        print(f'Setting {name} priority for {seconds_to_sleep} seconds')
        fun()
        sleep(seconds_to_sleep)

    set_normal()
    print('Done.')
