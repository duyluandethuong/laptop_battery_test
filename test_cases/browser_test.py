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
        'https://www.engadget.com/the-7-best-white-elephant-gifts-that-are-worth-stealing-150516076.html',
        'https://www.engadget.com/transportation/evs/tesla-is-recalling-almost-700000-vehicles-over-a-tire-pressure-monitor-issue-223639361.html',
        'https://www.engadget.com/entertainment/tv-movies/james-bond-the-movie-franchise-not-the-spy-may-be-in-deep-jeopardy-211608094.html',
        'https://www.engadget.com/cybersecurity/the-us-consumer-financial-protection-bureau-sues-zelle-and-four-of-its-partner-banks-175714692.html',
        'https://www.engadget.com/apps/flipboard-just-launched-surf-which-is-sort-of-like-an-rss-feed-for-the-open-social-web-184015833.html',
    ]

    for url in urls:
        webbrowser.open(url)

        time.sleep(2)

        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=1)
        pyautogui.click(clicks=1)

        custom_scroll(times=10, direction="down")

        time.sleep(10)

        custom_scroll(times=10, direction="up")

        time.sleep(10)

        custom_scroll(times=10, direction="down")

    # Close the browser:
    if is_windows:
        pyautogui.hotkey('alt', 'f4')

    if is_macos:
        pyautogui.hotkey('command', 'q')