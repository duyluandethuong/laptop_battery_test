import pyautogui
import os
import platform
from utils.battery_utils import get_battery_level
from utils import start_file, close_window
from utils import custom_scroll
import time

text_to_write = """
    Activity Requirements
    Each team in the class will be assigned one of the topics from the below list. The students will research and write a 700 word reflection report about it:
    1.	Identify a government initiative on IT, describe it and explain its impact on IT strategy.
    2.	Identify an economic factor (such as AEC - Asean Economic Community or TPP), describe it and explain its impact on IT strategy.
    3.	Identify a technology that will be soon commercialized, describe it and explain its impact on IT strategy.
"""

def run_office_test():
    base_path = os.path.join('test_files', 'office')

    file_paths = [
        os.path.join(base_path, 'word_test_1.docx'),
        os.path.join(base_path, 'word_test_2.docx'),
        os.path.join(base_path, 'word_test_3.docx'),
        os.path.join(base_path, 'excel_test_1.xlsx'),
    ]

    os_name = os.name
    platform_name = platform.system()

    print(f'Running Office Test on {os_name}, {platform_name}')
    get_battery_level()

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor
    print(f'Screen size: {screenWidth}, {screenHeight}')

    for path in file_paths:

        start_file(path)
        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=1)
        pyautogui.click(clicks=1)

        custom_scroll(times=10, direction="down")

        time.sleep(10)

        custom_scroll(times=10, direction="up")

        time.sleep(10)

        custom_scroll(times=10, direction="down")

        close_window()

        time.sleep(2)