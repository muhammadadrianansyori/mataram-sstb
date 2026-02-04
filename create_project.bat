@echo off
echo ==========================================
echo GOOGLE CLOUD PROJECT SETUP
echo ==========================================
echo.
echo This script will help you create a Google Cloud Project
echo which is REQUIRED for Google Earth Engine.
echo.
echo STEPS:
echo 1. This will open Google Cloud Console in your browser
echo 2. Click "CREATE PROJECT" button
echo 3. Enter project name: mataram-sstb
echo 4. Click "CREATE"
echo 5. Wait for project creation (30 seconds)
echo 6. Copy the PROJECT ID (usually: mataram-sstb-XXXXXX)
echo.
pause
echo.
echo Opening Google Cloud Console...
start https://console.cloud.google.com/projectcreate
echo.
echo After creating the project, please:
echo 1. Copy the PROJECT ID
echo 2. Run: setup_project.bat
echo.
pause
