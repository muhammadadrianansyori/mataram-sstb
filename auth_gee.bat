@echo off
echo ==========================================
echo Google Earth Engine Authentication (PROJECT FIX)
echo ==========================================
echo.
echo CRITICAL STEP:
echo When the browser opens, you MUST select a Cloud Project.
echo If you don't have one, click "Create a new Cloud Project".
echo.
REM Using --force to ensure the project selector appears
python -c "import ee; ee.Authenticate(force=True)"
echo.
echo Authentication finished. Try running start.bat now.
pause
