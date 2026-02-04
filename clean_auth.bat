@echo off
echo ==========================================
echo CLEANING GEE CREDENTIALS
echo ==========================================
echo.
echo Deleting old credential file...
del /F /Q "%USERPROFILE%\.config\earthengine\credentials"
echo.
echo Credentials wiped. Please run auth_gee.bat again.
echo.
pause
