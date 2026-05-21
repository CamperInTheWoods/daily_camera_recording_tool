@echo off
set SCRIPT=%~dp0recorder.py
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AutoRecorder.lnk

powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP%');$s.TargetPath='pythonw.exe';$s.Arguments='\"%SCRIPT%\"';$s.WorkingDirectory='%~dp0';$s.Save()"

echo [완료] 등록됨: %STARTUP%
echo 재부팅하면 자동으로 실행됩니다.
pause
