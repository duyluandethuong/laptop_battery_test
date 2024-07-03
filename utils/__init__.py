import os
import platform
import subprocess
import pyautogui

def start_file(file_path:str):
    platform_name = platform.system()

    if platform_name == "Windows":
        os.startfile(file_path)
    else:
        opener = "open" if platform_name == "Darwin" else "xdg-open"
        subprocess.call([opener, file_path])

def detect_platform():
    platform_name = platform.system()

    is_windows = True
    is_macos = False

    if platform_name == 'Darwin':
        is_windows = False
        is_macos = True

    return is_windows, is_macos

def close_window():
    is_windows, is_macos = detect_platform()

    if is_windows:
        pyautogui.hotkey('alt', 'f4')

    if is_macos:
        pyautogui.hotkey('command', 'q')