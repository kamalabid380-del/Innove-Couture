@echo off
title Innove Couture
cd /d "%~dp0"

set "PAGE=%~1"
if "%PAGE%"=="" set "PAGE=/"

rem Start the local server only if it is not already running
curl -s -o NUL -m 2 http://127.0.0.1:8000/ >nul 2>&1
if errorlevel 1 (
  wscript //nologo "%~dp0start-hidden.vbs"
  for /l %%i in (1,1,30) do (
    curl -s -o NUL -m 1 http://127.0.0.1:8000/ >nul 2>&1
    if not errorlevel 1 goto ready
    ping -n 2 127.0.0.1 >nul
  )
  echo.
  echo The server could not start. Details are in:
  echo   %~dp0server.log
  echo.
  pause
  exit /b 1
)

:ready
rem Open the site in its own window (Chrome first, then Edge, then default browser)
set "CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
set "PROFILE=%LOCALAPPDATA%\InnoveCoutureApp"

if exist "%CHROME%" (
  start "" "%CHROME%" --new-window http://127.0.0.1:8000%PAGE% --user-data-dir="%PROFILE%" --window-size=1500,960 --no-first-run --no-default-browser-check
  goto :done
)
if exist "%EDGE%" (
  start "" "%EDGE%" --new-window http://127.0.0.1:8000%PAGE% --user-data-dir="%PROFILE%" --window-size=1500,960 --no-first-run --no-default-browser-check
  goto :done
)
start "" http://127.0.0.1:8000%PAGE%
:done
