import pyautogui
import time
import webbrowser
import os
import platform
import logging

from utils.battery_utils import get_battery_level
from test_cases.office_test import run_office_test
from test_cases.browser_test import run_browser_test

# Disable fail safe mechanism of Pyautogui
pyautogui.FAILSAFE = False

logging.basicConfig(
    filename=f'logfilename.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

logging.info('====================== Starting new test... ====================')

os_name = os.name
platform_name = platform.system()

print(f'Running on {os_name}, {platform_name}')
get_battery_level()

is_windows = True
is_macos = False

while True:
    run_browser_test()
    run_office_test()
    get_battery_level()