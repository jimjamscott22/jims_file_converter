@echo off
REM Quick build script for Jim's File Converter
REM Double-click this file to build the executable

echo ====================================
echo Building Jim's File Converter
echo ====================================
echo.

REM Check if venv is activated
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if errorlevel 1 (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Could not activate virtual environment
        echo Please run: python -m venv venv
        pause
        exit /b 1
    )
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Could not install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Starting build process...
echo This may take a few minutes...
echo.

python build_exe.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ====================================
echo Build complete!
echo ====================================
echo.
echo Your executable is ready:
echo   dist\JimsFileConverter.exe
echo.
echo Don't forget to copy your .env file to the dist folder!
echo.
pause
