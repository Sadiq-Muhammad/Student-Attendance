@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Set the virtual environment directory name
SET VENV_DIR=venv

REM Create the virtual environment
python -m venv %VENV_DIR%

REM Check if the virtual environment was created successfully
IF NOT EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate the virtual environment
CALL "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip to the latest version
python -m pip install --upgrade pip

REM Install the required packages from requirements.txt
IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found. Skipping package installation.
)

REM Deactivate the virtual environment
deactivate
