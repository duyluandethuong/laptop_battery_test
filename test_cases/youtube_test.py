import pyautogui
import time
import webbrowser
import os
import platform
from utils.battery_utils import get_battery_level
from utils import close_window, sleep_with_mouse_activity

def run_youtube_test():

    os_name = os.name
    platform_name = platform.system()

    print(f'Running YouTube Test on {os_name}, {platform_name}')
    get_battery_level()

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor
    print(f'Screen size: {screenWidth}, {screenHeight}')

    # Browsing test
    urls = [
        'https://www.youtube.com/watch?v=MbXLt7OwEXI',
        'https://www.youtube.com/watch?v=w1ucZCmvO5c',
    ]

    for url in urls:
        get_battery_level()
        webbrowser.open(url)

        # Keep the mouse moving every 5 minutes so no screen saver kicks in
        sleep_with_mouse_activity(2 * 60 * 10, interval=5 * 60)

        get_battery_level()

    close_window()