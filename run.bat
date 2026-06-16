@echo off
REM Laptop Battery Test launcher (Windows)
REM Self-elevates to Administrator, syncs deps, then runs the test.
REM The test applies the one-click system setup (utils\system_setup.py)
REM automatically before the test loop starts.
REM
REM Usage:  run.bat        (full test, YouTube enabled)
REM         run.bat 1      (skip the YouTube test)

setlocal

REM --- Self-elevate to Administrator (powercfg / WMI brightness need it) ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    if "%~1"=="" (
        powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0'"
    ) else (
        powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    )
    exit /b
)

REM --- Run from the script's own directory ---
cd /d "%~dp0"

REM --- Check uv is available ---
where uv >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: uv is not installed!
    echo Install it with: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    pause
    exit /b 1
)

REM --- Sync dependencies ---
echo [1/2] Syncing dependencies...
uv sync
if %errorLevel% neq 0 (
    echo Error: Failed to sync dependencies!
    pause
    exit /b 1
)

REM --- Run the test (system setup runs first, inside start_test) ---
echo [2/2] Starting test...
uv run python -m test %*

pause
