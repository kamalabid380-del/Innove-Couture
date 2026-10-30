@echo off
title Restart Innove Couture
cd /d "%~dp0"

rem Stop whatever is serving the site on port 8000
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /c:":8000" ^| findstr /c:"LISTENING"') do taskkill /PID %%p /F >nul 2>&1
ping -n 2 127.0.0.1 >nul

call "%~dp0start.bat" %*
