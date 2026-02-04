@echo off
echo ==========================================
echo ENABLE EARTH ENGINE API
echo ==========================================
echo.
echo Project detected: mataram-sstb
echo.
echo Opening Earth Engine API enablement page...
echo.
echo LANGKAH:
echo 1. Browser akan terbuka
echo 2. Klik tombol "ENABLE" (biru)
echo 3. Tunggu 10-30 detik
echo 4. Setelah selesai, tutup browser
echo 5. Jalankan start.bat lagi
echo.
pause
echo.
start https://console.developers.google.com/apis/api/earthengine.googleapis.com/overview?project=mataram-sstb
echo.
echo Waiting for API enablement...
echo After clicking ENABLE, please wait and then close this window.
echo.
pause
