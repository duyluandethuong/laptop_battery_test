import pyautogui
import time
import webbrowser
import os
import platform
from utils.battery_utils import get_battery_level
from utils import custom_scroll

def run_browser_test():

    os_name = os.name
    platform_name = platform.system()

    print(f'Running Browser Test on {os_name}, {platform_name}')
    get_battery_level()

    is_windows = True
    is_macos = False

    if platform_name == 'Darwin':
        is_windows = False
        is_macos = True

    control_key_str = 'ctrl'

    if is_macos:
        control_key_str = 'command'

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor
    print(f'Screen size: {screenWidth}, {screenHeight}')

    # Browsing test
    urls = [
        'https://www.theverge.com/2024/7/2/24190823/figma-ai-tool-apple-weather-app-copy',
        'https://www.theverge.com/2024/7/2/24190641/apple-vision-pro-headset-future-cheaper',
        'https://www.theverge.com/2024/6/25/24185462/microsoft-surface-laptop-7th-edition-review',
        'https://www.theverge.com/23350899/nintendo-switch-controllers-best-wireless-joy-con-gamepad',
        'https://www.theverge.com/24185290/beats-pill-2024-bluetooth-speaker-review',
    ]

    for url in urls:
        webbrowser.open(url)

        time.sleep(2)

        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=1)
        pyautogui.click(clicks=1)

        custom_scroll(times=10, direction="down")

        custom_scroll(times=10, direction="up")

    # Close the browser:
    if is_windows:
        pyautogui.hotkey('alt', 'f4')

    if is_macos:
        pyautogui.hotkey('command', 'q')

    get_battery_level()