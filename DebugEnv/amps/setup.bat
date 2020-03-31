python -m virtualenv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
ECHO You are now in venv!
ECHO Execute scripts from inside venv, to avoid dependency errors
ECHO Execute \venv\Scripts\activate.bat to return to venv, should you close this window!
@PAUSE
