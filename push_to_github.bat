@echo off
set REPO_URL=https://github.com/duyluandethuong/laptop_battery_test
set COMMIT_MSG=Update laptop battery test application

echo ============================================
echo Pushing code to %REPO_URL%
echo ============================================

REM Check if git is available
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: git is not installed or not in the PATH.
    echo Please install Git for Windows and try again.
    pause
    exit /b 1
)

REM Initialize git if needed
if not exist .git (
    echo Initializing new git repository...
    git init
    git branch -M main
)

REM Remote check
git remote -v | findstr "origin" >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Remote origin exists, updating URL...
    git remote set-url origin %REPO_URL%
) else (
    echo Adding remote origin...
    git remote add origin %REPO_URL%
)

echo ============================================
echo Done!
pause
