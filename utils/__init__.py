import os
import platform
import subprocess
import time
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

def custom_scroll(times=1, direction="down"):
    scrolling_distance = 10
    is_windows, is_macos = detect_platform()

    if is_windows:
        scrolling_distance = 150

    if direction == 'down':
        scrolling_distance = scrolling_distance * -1

    scroll_time = 1
    while scroll_time <= times:
        pyautogui.scroll(scrolling_distance)
        scroll_time += 1

def nudge_mouse():
    """Move the mouse a little and back, so the OS does not see the machine as idle."""
    screen_width, _ = pyautogui.size()
    current_x, current_y = pyautogui.position()

    # Nudge towards whichever side keeps the pointer on screen
    offset = 50 if current_x + 50 < screen_width else -50

    pyautogui.moveTo(current_x + offset, current_y, duration=0.5)
    pyautogui.moveTo(current_x, current_y, duration=0.5)

def sleep_with_mouse_activity(seconds, interval=5 * 60):
    """Sleep for `seconds`, nudging the mouse every `interval` seconds.

    Some laptops start a screen saver / dim the screen when there is no input,
    which would make the battery test inaccurate, so the mouse has to keep moving
    even while a video is playing on its own.
    """
    remaining = seconds

    while remaining > 0:
        chunk = min(interval, remaining)
        time.sleep(chunk)
        remaining -= chunk
        nudge_mouse()
