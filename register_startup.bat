@echo off
:: 현재 폴더의 recorder.py를 Windows 시작 프로그램에 등록합니다.
set SCRIPT_PATH=%~dp0recorder.py
set SHORTCUT_NAME=AutoRecorder

:: 시작 프로그램 폴더에 VBScript로 바로가기 생성
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VBS_TEMP=%TEMP%\create_shortcut.vbs

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_TEMP%"
echo sLinkFile = "%STARTUP_DIR%\%SHORTCUT_NAME%.lnk" >> "%VBS_TEMP%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_TEMP%"
echo oLink.TargetPath = "pythonw.exe" >> "%VBS_TEMP%"
echo oLink.Arguments = """%SCRIPT_PATH%""" >> "%VBS_TEMP%"
echo oLink.WorkingDirectory = "%~dp0" >> "%VBS_TEMP%"
echo oLink.Description = "Auto Camera Recorder" >> "%VBS_TEMP%"
echo oLink.Save >> "%VBS_TEMP%"

cscript //nologo "%VBS_TEMP%"
del "%VBS_TEMP%"

echo [완료] 시작 프로그램에 등록되었습니다: %STARTUP_DIR%\%SHORTCUT_NAME%.lnk
echo 컴퓨터를 재시작하면 자동으로 실행됩니다.
pause
