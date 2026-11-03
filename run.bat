@echo off
setlocal EnableExtensions
pushd "%~dp0"

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
REM Load the project source from this folder even after moving it.
set "PYTHONPATH=%~dp0src;%PYTHONPATH%"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Khong tim thay moi truong Python tai: "%PYTHON_EXE%"
    echo Hay tao moi truong truoc:
    echo   py -3.11 -m venv .venv
    echo   .\.venv\Scripts\python.exe -m pip install -r requirements-vision.lock.txt
    echo   .\.venv\Scripts\python.exe -m pip install -e .
    popd
    exit /b 1
)

REM Neu co truyen tham so (vd: run.bat preview, run.bat check, run.bat test)
if not "%~1"=="" goto CLI_MODE

:MENU
cls
echo ============================================================
echo   HAND-TRACKING - MENU CHAY NHANH
echo ============================================================
echo   [1] Xem truoc camera va landmark (preview)
echo   [2] Kiem tra cau hinh va moi truong (check)
echo   [3] Thu du lieu pilot_01 (train, 10 clip/nhan)
echo   [4] Thu du lieu tuy chinh (nhap session/split/count/label)
echo   [5] Kiem tra du lieu da thu (dataset-check)
echo   [6] Chay unit tests (unittest)
echo   [0] Thoat
echo ============================================================
set "CHOICE="
set /p "CHOICE=Chon chuc nang (0-6): "

if "%CHOICE%"=="1" goto DO_PREVIEW
if "%CHOICE%"=="2" goto DO_CHECK
if "%CHOICE%"=="3" goto DO_COLLECT_PILOT
if "%CHOICE%"=="4" goto DO_COLLECT_CUSTOM
if "%CHOICE%"=="5" goto DO_DATASET_CHECK
if "%CHOICE%"=="6" goto DO_TEST
if "%CHOICE%"=="0" goto EXIT_CLEAN

echo Lua chon khong hop le!
timeout /t 1 >nul
goto MENU

:DO_PREVIEW
echo.
"%PYTHON_EXE%" -m hand_tracking preview
echo.
pause
goto MENU

:DO_CHECK
echo.
"%PYTHON_EXE%" -m hand_tracking check
echo.
pause
goto MENU

:DO_COLLECT_PILOT
echo.
"%PYTHON_EXE%" -m hand_tracking collect --session pilot_01 --split train --count 10
echo.
pause
goto MENU

:DO_COLLECT_CUSTOM
echo.
set "SESSION=pilot_01"
set "SPLIT=train"
set "COUNT=10"
set "LABEL="
set /p "SESSION=Nhap ten session [mac dinh: pilot_01]: "
set /p "SPLIT=Nhap split (train/validation/test) [mac dinh: train]: "
set /p "COUNT=Nhap so clip moi nhan [mac dinh: 10]: "
set /p "LABEL=Nhap nhan cu the (bo trong = thu ca 5 nhan): "
echo.
if "%LABEL%"=="" (
    "%PYTHON_EXE%" -m hand_tracking collect --session "%SESSION%" --split "%SPLIT%" --count %COUNT%
) else (
    "%PYTHON_EXE%" -m hand_tracking collect --session "%SESSION%" --split "%SPLIT%" --count %COUNT% --label "%LABEL%"
)
echo.
pause
goto MENU

:DO_DATASET_CHECK
echo.
set "CHECK_SPLIT=train"
set /p "CHECK_SPLIT=Nhap split can kiem tra (train/validation/test) [mac dinh: train]: "
echo.
"%PYTHON_EXE%" -m hand_tracking dataset-check --split "%CHECK_SPLIT%"
echo.
pause
goto MENU

:DO_TEST
echo.
"%PYTHON_EXE%" -m unittest discover -s tests -v
echo.
pause
goto MENU

:CLI_MODE
if /I "%~1"=="test" goto CLI_TEST
"%PYTHON_EXE%" -m hand_tracking %*
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%

:CLI_TEST
shift
"%PYTHON_EXE%" -m unittest discover -s tests -v %1 %2 %3 %4 %5 %6 %7 %8 %9
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%

:EXIT_CLEAN
popd
exit /b 0
