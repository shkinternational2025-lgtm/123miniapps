@echo off
title 123MiniApps - local server
cd /d "%~dp0"

echo(
echo   ===============================================
echo      Starting the 123MiniApps local server
echo   ===============================================
echo(
echo   Folder : %CD%
echo   URL    : http://localhost:8000/
echo(
echo   A browser window will open automatically in a moment.
echo   Keep THIS window open while you use the site.
echo   Close it (or press Ctrl+C) to stop the server.
echo(

REM ---- Detect Python (its built-in server is the most reliable) ----
set "PYEXE="
where py >nul 2>nul && set "PYEXE=py -3"
if not defined PYEXE where python >nul 2>nul && set "PYEXE=python"

if defined PYEXE goto usepython
goto useps

:usepython
echo   Using Python's built-in web server.
echo(
REM Open the browser 2 seconds later (gives the server time to start).
start "" powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000/'"
%PYEXE% -m http.server 8000 --bind 127.0.0.1
goto done

:useps
echo   Python not found - using the built-in Windows PowerShell server.
echo(
powershell -NoProfile -Command "try{ Unblock-File -LiteralPath '%~dp0serve.ps1' -ErrorAction SilentlyContinue }catch{}" >nul 2>nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1"
goto done

:done
echo(
echo   The server has stopped. You can close this window.
pause >nul
