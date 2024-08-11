import pyautogui
import time
import multiprocessing
import os
import platform
import logging
import argparse

from utils.battery_utils import get_battery_level
from test_cases.office_test import run_office_test
from test_cases.browser_test import run_browser_test
from test_cases.youtube_test import run_youtube_test

# Disable fail safe mechanism of Pyautogui
pyautogui.FAILSAFE = False

logging.basicConfig(
    filename=f'logfilename.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

def start_test(no_youtube='0'):
    logging.info('====================== Starting new test... ====================')
    if (no_youtube == '1'):
        youtube_message = 'YouTube test is disabled'
    else:
        youtube_message = 'YouTube test is enable'

    print(youtube_message)
    logging.info(youtube_message)

    os_name = os.name
    platform_name = platform.system()

    print(f'Running on {os_name}, {platform_name}')
    get_battery_level()

    while True:
        run_browser_test()
        run_office_test()

        if str(no_youtube) != '1':
            run_youtube_test()

def information_process():
    while True:
        get_battery_level()
        time.sleep(3)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Run a script and measure battery life")
    parser.add_argument("no_youtube", nargs='?', choices=['1', '0'], default='0')

    args = parser.parse_args()

    p1 = multiprocessing.Process(target=start_test, args=(args.no_youtube))
    p2 = multiprocessing.Process(target=information_process)
    p1.start()
    p2.start()