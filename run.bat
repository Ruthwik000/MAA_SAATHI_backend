@echo off
echo Starting VitalSync Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check for Firebase credentials
if not exist "serviceAccountKey.json" (
    echo Warning: serviceAccountKey.json not found!
    echo Please add your Firebase service account key before running.
    pause
    exit /b 1
)

REM Start server
echo.
echo Starting server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
