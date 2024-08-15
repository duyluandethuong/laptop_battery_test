# Laptop Battery Test

This test aims to simulate a series of office-related tasks, such as web browsing, opening and scrolling MS Office files... in order to test how long a laptop's battery may last.

The result is constantly written to a log file so you do not have to worry about losing your test. The test file will only be saved on the disk, with the accuracy of +- 1-2 minutes, not a lot (and it can be improved in the future).

# Supported OS

- Windows 11 x86 / x64
- Windows 11 ARM 64-bit
- macOS 12 ARM 64-bit

The author has tested this program on several laptops running a wide variety of CPUs, including Intel Core Ultra, Snapdragon X Elite, Apple M-Series

# Required third party software

- Python: to run the script
- A default browser: Edge, Safari, or any default browser of your choice. Edge and Safari are recommended since they are default browser for most Windows and Mac machine
- Microsoft Office: Word, Excel, PowerPoint

# Tasks to perform

The program will run infinite loop of the following tasks
1. Open 5 websites using default browser
2. Open 3 Word files and 1 Excel files

There will be scrolling and mouse moving when running the test.

In the future, text input will be added to better resemble how a normal user would use an Office app.

# Before you run any test, check all boxes in this checklist

Use this checklist and you can make sure all tests are consistent
- [ ] Set laptop's screen brightness to 75% (on Mac, you can ask Siri "Set screen brightness to 75% for an accurate setting)
- [ ] Turn off auto turn off screen on battery power
- [ ] Connect your laptop to Wifi network, turn on Bluetooth
- [ ] Leave battery saver mode on if your laptop have it, set battery saver on at 30% (30% is the default settings for Windows in recent updates)
- [ ] Turn lower screen brightness on low battery off
- [ ] Turn the volume to 0%
- [ ] Charge your laptop to 100% battery

# How to run

## Installation

1. Install Python https://www.python.org/downloads/
2. Download this code by click on the Code (green button) > Download ZIP, or you can use `git clone` this repo to your machine.
3. Unzip the ZIP file you have just download
4. Open Command Prompt (cmd) and navigate to your extracted folder (e.g: `cd C:\Users\Duyluan\Downloads\laptop_battery_test`)

## Run the program

**Always navigate to project folder first**

### macOS:

Open Terminal and run the following commands

```sh
python3 -m venv battery_test_env
source battery_test_env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 -m test
```

**You only need to do it once, on the first time**. For the following runs, you only need to run these code

```sh
source battery_test_env/bin/activate
python3 -m test
```

### Windows:

Note: You must run the following commands in Command Prompt (CMD), do not run on PowerShell
(You may need to install C++ Builds Tools if the error show when building wheels. Check the error message to see if you need to do so)

```sh
python -m venv battery_test_env
battery_test_env\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python -m test
```

**You only need to do it once, on the first time**. For the following runs, you only need to run these code

```sh
battery_test_env\Scripts\activate.bat
python -m test
```

# Disable YouTube test

By default, the script will run with YouTube playback test included, if you want to disable the YouTube playback, run

```sh
python -m test 1
```

# How to calculate time difference

After the laptop is shutdown due to low battery, charge your laptop and power it on. Go to this project folder, you will find a file called `logfilename.log`. It records the entire testing duration. When you open the file, you will see the timestamps that have been logged by the script.

To calculate the time difference between the start and end time:

**macOS**:

```sh
python3 datetime_calculator.py "your start timestamp" "your end timestamp"
```

**Windows**:

```sh
python datetime_calculator.py "your start timestamp" "your end timestamp"
```

In the future, I will make it easier to see the time difference.

# Next steps:
- Build a system to store the log file and allow users to search for laptop's battery test result

# How to develop:

Pull the repo, then follow the instruction above. You should start checking the `test.py` file, it is the entry file for the whole script.
I'm thinking changing it to a __main__ script

# Trouble shooting, Q&A:

**Q: Cannot run Python in command prompt?**
A: If you open the command prompt before you install Python, the `python` command has not been registered to PATH. Simply close command prompt or open a new tab will solve the issue.

