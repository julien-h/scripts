# Julien-h's scripts

This repo contains the bash and python scripts I wrote when using Windows 10 OS.

## Index

- **wslenv**: bash script to translate a windows environment var such as `%PATH%` to a WSL one such as `$PATH`
- **process_priority.py**: python script to change to current thread's priority class
- **windows_notifier.py**: python script to display a native windows 10 toast notification from windows python or WSL python
- **slack_notifier.py**: python script to send a notification on a slack channel specified in `SLACK_NOTIFIER_URL' environment variable
- **email_notifier.py**: python script to send a notification by email to a pre-configured destination address
- **selenium_tools.py**: python library that adds missing features to Selenium, such as ability to download files
- **download.py**: download a file and display an optional progress bar
- **low_level_keyboard_hook.py**: an implementation of LowLevelKeyboardHook for Windows DLL, use it to listen to keyboard events
- **nightlight.py**: functions to open the nightlight settings on Windows and send input to it
- **nightlight_hotkey.py**: implement a hotkey to change nightlight settings; does so by listening to keyboard input

## Disclaimer

I have since switched to Linux and haven't published my new set of scripts, yet. Send me a mail if you want to see them on Github.
