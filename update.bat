@echo off
REM ===================================================================
REM  halal-graphify - update this PC to the newest upstream release
REM
REM  Double-click this file. It will:
REM    1. pull anything the weekly GitHub sync already did
REM    2. check upstream for a newer release and regenerate if there is one
REM    3. push that back to your fork
REM    4. install the result on this computer
REM
REM  Safe to run any time. If nothing has changed it says so and stops.
REM ===================================================================

setlocal
cd /d "%~dp0"

echo.
echo === 1/4  Pulling your fork ===============================
git pull --ff-only
if errorlevel 1 goto :failed

echo.
echo === 2/4  Checking upstream ===============================
python sync.py
if errorlevel 1 goto :guard_failed

echo.
echo === 3/4  Pushing to your fork ============================
git push --follow-tags
if errorlevel 1 echo    (nothing to push, or push declined - continuing)

echo.
echo === 4/4  Installing on this computer =====================
python -m pip install --upgrade --force-reinstall .
if errorlevel 1 goto :failed

echo.
echo === Done ================================================
halal-graphify --version
echo.
echo The original 'graphify' command is untouched and still works.
goto :end

:guard_failed
echo.
echo *** STOPPED - nothing was published. ***
echo.
echo Upstream has introduced wording this fork does not know how to
echo rename yet, so it refused to ship it. The lines above show
echo exactly which file and line caused it.
echo.
goto :end

:failed
echo.
echo *** Something went wrong. Nothing was installed. ***
echo See the messages above.
echo.

:end
echo.
pause
endlocal
