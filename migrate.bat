@echo off
REM ===================================================================
REM  halal-graphify - convert a project that used the original Graphify
REM
REM  Put this file inside the project you want to convert and
REM  double-click it. It converts the graph data in graphify-out/ so
REM  your existing graph keeps working - no need to re-extract.
REM
REM  Your own notes and documents are NOT touched unless you ask for
REM  them, and even then it shows you every change and waits for you
REM  to type y before writing anything.
REM ===================================================================

setlocal
cd /d "%~dp0"

echo.
echo Converting graph data in: %CD%
echo.

halal-graphify migrate .
if errorlevel 1 goto :failed

echo.
echo -------------------------------------------------------------
echo  Graph data done. Backups were saved next to each file (.bak).
echo -------------------------------------------------------------
echo.
set /p DOCS="Also check your own notes and documents? [y/N] "
if /i not "%DOCS%"=="y" goto :end

echo.
halal-graphify migrate . --docs
goto :end

:failed
echo.
echo *** Could not run halal-graphify. ***
echo.
echo Is it installed? Install it with:
echo     pip install halal-graphify
echo.

:end
echo.
pause
endlocal
