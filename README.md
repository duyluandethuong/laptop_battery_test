
macOS:

python3 -m venv battery_test
source battery_test/bin/activate

Windows:

python3 -m venv battery_test
battery_test/Scripts/Activate.ps1

Install dependencies

battery_test/bin/pip install -r requirements.txt

Run:

macOS:
pip3 install -r requirements.txt
python3 -m test

Windows:
(You may need to install C++ Builds Tools if the error show when building wheels. Check the error message to see if you need to do so)

pip install -r requirements.txt
python -m test