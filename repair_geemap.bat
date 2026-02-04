@echo off
echo ==========================================
echo REPAIR GEEMAP VERSION
echo ==========================================
echo.
echo The installed version of 'geemap' (v0.30+) has a known conflict
echo with your Python environment.
echo.
echo Downgrading to stable version v0.29.6...
python -m pip uninstall -y geemap python-box
python -m pip install "geemap==0.29.6" "python-box==6.1.0"
echo.
echo ==========================================
echo Repair Complete.
echo Please run 'start.bat' again.
echo ==========================================
pause
