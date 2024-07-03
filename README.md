# Laptop Battery Test

This test aims to simulate a series of office-related tasks, such as web browsing, opening and scrolling MS Office files... in order to test how long a laptop's battery may last.

The result is constantly written to a log file so you do not have to worry about losing your test. The test file will only be saved on the disk, with the accuracy of +- 1-2 minutes, not a lot (and it can be improved in the future).

# Supported OS

- Windows 11 x86 / x64
- Windows 11 ARM 64-bit
- macOS 12 ARM 64-bit

The author has tested this program on several laptops running a wide variety of CPUs, including Intel Core Ultra, Snapdragon X Elite, Apple M-Series

# List of tasks

The program will run infinite loop of the following tasks
1. Open 5 websites using default browser
2. Open 3 Word files and 1 Excel files

There will be scrolling and mouse moving when running the test.

In the future, text input will be added to better resemble how a normal user would use an Office app.

# How to run

## Installation

1. Install Python https://www.python.org/downloads/
2. Download this code by click on the Code (green button) > Download ZIP, or you can use `git clone` this repo to your machine.
3. Unzip the ZIP file you have just download
4. Open Command Prompt (cmd) and navigate to your extracted folder (e.g: `cd C:\Users\Duyluan\Downloads\laptop_battery_test`)

## Prepare the program

### macOS:

Open Terminal and run the following commands

```
python3 -m venv battery_test_env
source battery_test_env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 -m test
```

### Windows:

Note: You must run the following commands in Command Prompt (CMD), do not run on PowerShell
(You may need to install C++ Builds Tools if the error show when building wheels. Check the error message to see if you need to do so)

```
python -m venv battery_test_env
battery_test_env\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python -m test
```

# Next steps:
- Package the script into a single executable files
- Add more tests to better simulate real world office use
- Change the test files into a larger one
- Add some test on Youtube video playback (perhaps?)

# How to develop:

Pull the repo, then follow the instruction above. You should start checking the `test.py` file, it is the entry file for the whole script.
I'm thinking changing it to a __main__ script
