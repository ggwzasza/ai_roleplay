@echo off
title Build Android APK
echo ========================================
echo   AI Roleplay - Android APK Builder
echo ========================================
echo.

where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker not found!
    echo.
    echo Please install Docker Desktop first:
    echo   https://www.docker.com/products/docker-desktop/
    echo.
    echo Alternative: Use GitHub Actions (push to GitHub and the APK will be built automatically)
    echo.
    pause
    exit /b 1
)

echo [1/3] Building Docker image...
docker build -t ai-roleplay-builder .

echo [2/3] Building APK inside container...
docker run --rm -v "%cd%\bin":/app/bin ai-roleplay-builder

echo [3/3] Done!
echo.
if exist "bin\*.apk" (
    echo APK file(s) found in bin\ directory:
    dir /b bin\*.apk
) else (
    echo [WARNING] APK not found in bin\. Check the build output above for errors.
)
echo.
pause
