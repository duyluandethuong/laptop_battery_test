
macOS:

python3 -m venv battery_test
source battery_test/bin/activate

Windows:

Run in cmd, do not run on PowerShell

battery_test\Scripts\activate.bat

Install dependencies

battery_test/bin/pip install -r requirements.txt

<<<<<<< HEAD
PowerShell note

Open PowerShell as an Administrator
Type Set-ExecutionPolicy Unrestricted
Press Enter
Type A
Run the PowerShell script
Once finished, type Set-ExecutionPolicy Restricted
Press Enter
Type Exit
=======
Run:

macOS:
pip3 install -r requirements.txt
python3 -m test

Windows:
(You may need to install C++ Builds Tools if the error show when building wheels. Check the error message to see if you need to do so)

pip install -r requirements.txt
python -m test
>>>>>>> 15e1a4f6cd38295f841239b0d28e0e9694b42a06
