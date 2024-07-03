
macOS:

python3 -m venv battery_test_env
source battery_test_env/bin/activate
pip3 install --upgrade pip

Windows:

Run in cmd, do not run on PowerShell

python -m venv battery_test_env
battery_test_env\Scripts\activate.bat
pip install --upgrade pip

Install dependencies

battery_test_env/bin/pip install -r requirements.txt

Run:

macOS:
pip3 install -r requirements.txt
python3 -m test

Windows:
(You may need to install C++ Builds Tools if the error show when building wheels. Check the error message to see if you need to do so)

pip install -r requirements.txt
python -m test
