@echo off
echo ==========================================
echo FINAL REPAIR - Mataram SSTB Dependencies
echo ==========================================
echo.
echo Uninstalling conflicting libraries...
python -m pip uninstall -y geemap python-box xyzservices
echo.
echo Reinstalling stable compatible versions...
REM geemap 0.30+ should handle newer stuff, but let's stick to a safe combo
REM python-box 6.1.0 is safe.
REM xyzservices 2024.4.0 is safe.
python -m pip install "python-box==6.1.0" "xyzservices==2024.4.0" "geemap>=0.30.0"
echo.
echo ==========================================
echo Repair Complete.
echo Please closing ALL windows and run 'start.bat' again.
echo ==========================================
pause
