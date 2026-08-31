@echo off
title 123MiniApps - push changes to GitHub
cd /d "%~dp0"

where git >nul 2>nul || (
  echo(
  echo   Git is not installed. Download it from https://git-scm.com/ first,
  echo   then run this again.
  echo(
  pause
  exit /b
)

echo(
echo   ============================================
echo      Push 123MiniApps changes to GitHub
echo   ============================================
echo(

REM First run only: initialise the repo if it isn't one yet.
if not exist ".git" (
  echo   Setting up Git for the first time...
  git init
  git branch -M main
  echo(
  echo   NOTE: This folder is not yet linked to a GitHub repo.
  echo   1) Create an empty repo on github.com
  echo   2) Run this once (replace YOU/REPO):
  echo        git remote add origin https://github.com/YOU/REPO.git
  echo   Then run this file again.
  echo(
)

set "MSG=update"
set /p "MSG=  Describe this change (or press Enter for 'update'): "

git add .
git commit -m "%MSG%"
git push

echo(
echo   Done. If auto-deploy is set up, your VPS will update shortly.
echo(
pause
