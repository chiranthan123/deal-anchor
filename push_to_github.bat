@echo off
setlocal
echo ====================================================
echo DealAnchor - Push to GitHub
echo ====================================================
echo.
set /p REPO_URL="Enter your GitHub repository URL (e.g. https://github.com/username/deal-anchor.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Aborting.
    pause
    exit /b
)

echo.
echo Configuring remote and pushing to %REPO_URL% ...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================
    echo SUCCESS! DealAnchor has been pushed to your GitHub!
    echo ====================================================
) else (
    echo.
    echo [ERROR] Push failed. Please verify the URL and your GitHub permissions.
)

pause
