@echo off
rem *** Run this (double-click) to create an Windows .exe file with py2exe

rem ***** get rid of all the old files in the build folder
rd /S /Q build

rem windows magic to get version number from Python call into VERSION variable
rem stolen from:
rem http://www.tomshardware.co.uk/forum/230090-35-windows-batch-file-output-program-variable

setlocal enableextensions
for /f "tokens=*" %%a in (
'python -c "execfile('kurzfile/release.py'); print version"'
) do (
set VERSION=%%a
)
echo/%%VERSION%%=%VERSION%

rem ***** create the exe
python setup.py py2exe
rem create the installer
makensis /DVERSION=%VERSION% tools/kurzfile.nsi
endlocal
@echo on

rem **** pause so we can see the exit codes
pause "Done...hit a key to exit"
