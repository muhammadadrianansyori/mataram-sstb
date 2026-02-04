@echo off
echo ==========================================
echo Fixing Application Dependencies
echo ==========================================
echo.
echo Detected version conflict with 'python-box'.
echo Downgrading to compatible version...
echo.
python -m pip install "python-box<7"
echo.
echo ==========================================
echo Fix applied successfully!
echo Please close this window and run start.bat again.
echo ==========================================
pause
