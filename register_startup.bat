@echo off
chcp 65001 > nul
set SCRIPT_PATH=%~dp0recorder.py
set SHORTCUT_NAME=AutoRecorder
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VBS_TEMP=%TEMP%\create_shortcut.vbs

(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%STARTUP_DIR%\%SHORTCUT_NAME%.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "pythonw.exe"
echo oLink.Arguments = """%SCRIPT_PATH%"""
echo oLink.WorkingDirectory = "%~dp0"
echo oLink.Description = "Auto Camera Recorder"
echo oLink.Save
) > "%VBS_TEMP%"

cscript //nologo "%VBS_TEMP%"
del "%VBS_TEMP%"

echo [완료] 등록됨: %STARTUP_DIR%\%SHORTCUT_NAME%.lnk
echo 재부팅하면 자동으로 실행됩니다.
pause
