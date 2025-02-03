@echo off
REM install.bat: Install Python dependencies and check for external tools on Windows.

REM --- Step 1: Check for Python ---
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.6+.
    pause
    exit /b 1
)
echo Python found:
python --version

REM --- Step 2: Create a Virtual Environment (if not already created) ---
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

REM --- Step 3: Activate the Virtual Environment ---
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM --- Step 4: Upgrade pip ---
echo Upgrading pip...
python -m pip install --upgrade pip

REM --- Step 5: Install Python Dependencies ---
echo Installing Python dependencies from requirements.txt...
pip install -r requirements.txt
echo Python dependencies installed.

REM --- Step 6: Check for External Tools ---
echo.
echo Checking for external tools required for additional file conversions...
REM Define the external dependencies to check.
setlocal enabledelayedexpansion
set "deps=libreoffice wkhtmltopdf pdflatex ebook-convert"
for %%d in (%deps%) do (
    where %%d >nul 2>&1
    if errorlevel 1 (
        echo Warning: %%d is not installed or not in PATH. Some conversions may not work.
    ) else (
        echo %%d is installed.
    )
)
endlocal

echo.
echo Installation complete!
echo To activate the virtual environment in future sessions, run:
echo    call venv\Scripts\activate.bat
pause
