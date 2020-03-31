# because i want less files in the repo XD
# this is tested on windows
import os
import platform

def winsetup():
    os.system("python -m virtualenv venv & venv\\Scripts\\activate.bat & pip install -r requirements.txt & exit")
    print("Use the virtualenv")
def unixsetup():
    os.system("python -m virtualenv venv ; chmod +x venv/bin/activate ; . venv/bin/activate ; pip install -r requirements.txt")
sysos = platform.system()
if sysos == "Windows":
    winsetup()
elif sysos == "Linux" or os == "Darwin":
    unixsetup()
else:
    print("Unknown operating system.")
