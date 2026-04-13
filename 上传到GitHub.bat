@echo off
title GitHub Upload
echo ========================================
echo   Upload to GitHub
echo ========================================
echo.

set /p NAME="Enter your GitHub username: "
set /p REPO="Enter repository name (e.g., ai_roleplay): "

set REPO_URL=https://github.com/%NAME%/%REPO%.git

cd /d "%~dp0"

echo.
echo [1/6] Configuring git...
git config --global user.email "%NAME%@github.com"
git config --global user.name "%NAME%"

echo [2/6] Adding remote...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [3/6] Checking for commits...
git rev-parse HEAD >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo No commits found. Creating initial commit...
    git add -A
    git commit -m "Initial commit - AI Roleplay App"
)

echo [4/6] Checking branches...
git branch -a | findstr /C:"main" >nul
if %ERRORLEVEL% neq 0 (
    git branch -a | findstr /C:"master" >nul
    if %ERRORLEVEL% neq 0 (
        echo No main or master branch. Creating main branch...
        git branch -M main
    )
)

echo.
echo Current status:
git status --short
echo.

set /p CONFIRM="Commit and push? (y/n): "
if /i not "%CONFIRM%"=="y" exit /b 0

echo [5/6] Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% neq 0 (
    echo.
    echo Push failed. Trying force push...
    git push -u origin main --force
)

echo [6/6] Done!
echo.
echo Repository: %REPO_URL%
echo.
echo Now go to GitHub:
echo   1. Go to %REPO_URL%
echo   2. Click Actions
echo   3. Click "Build Android APK"
echo   4. Click "Run workflow"
echo.
pause
