@echo off
REM Build script for Laptop Battery Test (Windows)
REM Creates a standalone executable using PyInstaller

setlocal enabledelayedexpansion

set APP_NAME=LaptopBatteryTest

echo.
echo === Laptop Battery Test Build Script (Windows) ===
echo.

REM 1. Check prerequisites
echo [1/4] Checking prerequisites...

if not exist "%APP_NAME%.spec" (
    echo Error: %APP_NAME%.spec file not found!
    exit /b 1
)

where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: uv is not installed!
    echo Please install uv first: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    exit /b 1
)

echo OK All prerequisites found
echo.

REM 2. Clean previous builds
echo [2/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo OK Cleaned build and dist directories
echo.

REM 3. Sync dependencies
echo [3/4] Syncing dependencies...
uv sync
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to sync dependencies!
    exit /b 1
)

REM Add pyinstaller as dev dependency if not present
uv add --dev pyinstaller
echo.

REM 4. Build with PyInstaller
echo [4/4] Building application with PyInstaller...
uv run pyinstaller %APP_NAME%.spec --clean --noconfirm

if exist "dist\%APP_NAME%\%APP_NAME%.exe" (
    echo.
    echo === Build Successful! ===
    echo Executable location: dist\%APP_NAME%\%APP_NAME%.exe
    echo.
    echo You can distribute the entire 'dist\%APP_NAME%' folder.
) else (
    echo.
    echo Error: Build failed! Executable not found.
    exit /b 1
)

echo.
echo === Build Process Complete ===
pause
