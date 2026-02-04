@echo off
echo ==========================================
echo SETUP PROJECT ID
echo ==========================================
echo.
set /p PROJECT_ID="Enter your Google Cloud PROJECT ID: "
echo.
echo Setting up authentication with project: %PROJECT_ID%
echo.
python -c "import ee; ee.Authenticate(project='%PROJECT_ID%', force=True)"
echo.
echo Now updating utils.py with your project ID...
echo.
python -c "import re; content = open('utils.py', 'r', encoding='utf-8').read(); new_content = re.sub(r'ee\.Initialize\(\)', 'ee.Initialize(project=\"%PROJECT_ID%\")', content); open('utils.py', 'w', encoding='utf-8').write(new_content); print('✓ utils.py updated!')"
echo.
echo ==========================================
echo Setup Complete!
echo Please run start.bat now.
echo ==========================================
pause
