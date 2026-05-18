@echo off
echo [1/2] 패키지 설치 중...
pip install -r requirements.txt

echo.
echo [2/2] 완료. recorder.py를 실행하려면:
echo   python recorder.py
echo.
echo [선택] 컴퓨터 시작 시 자동 실행을 등록하려면:
echo   register_startup.bat 을 실행하세요.
pause
