@echo off
REM Windows batch file to build the project
REM This is a simple wrapper for the PowerShell script

powershell.exe -ExecutionPolicy Bypass -File "%~dp0build.ps1" %*

