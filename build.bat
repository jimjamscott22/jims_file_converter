@echo off
REM Quick build script for Jim's File Converter using uv
REM Double-click this file to build the executable

echo ====================================
echo Building Jim's File Converter
echo ====================================
echo.

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: uv is not installed
    echo Install it from: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo.
echo Syncing project and development dependencies...
uv sync --group dev
if errorlevel 1 (
    echo ERROR: Could not sync dependencies with uv
    pause
    exit /b 1
)

echo.
echo Starting build process...
echo This may take a few minutes...
echo.

uv run python build_exe.py

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
