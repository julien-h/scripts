import sys
import subprocess
from iswsl import is_wsl

win32 = (sys.platform == 'win32')


def linux_path(windows_path):
    return windows_path.replace('C:', '/mnt/c').replace('\\', '/')


def powershell_toast(title, msg):
    powershell = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
    icon = r'C:\Users\julien\Pictures\system\python.ico'

    if not win32 and is_wsl():
        powershell = linux_path(powershell)

    cmd = f'New-BurntToastNotification -AppLogo {icon} -Text "{title}","{msg}"'

    p = subprocess.Popen([powershell, cmd],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, error = p.communicate()
    rc = p.returncode
    return rc, output, error


def notify(msg, title='Python script'):
    powershell_toast(title, msg)
