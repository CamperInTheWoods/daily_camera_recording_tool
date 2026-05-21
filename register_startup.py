import sys
import winreg
from pathlib import Path

pythonw = Path(sys.executable).parent / "pythonw.exe"
script  = Path(__file__).parent / "recorder.py"
command = f'"{pythonw}" "{script}"'

key = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    0, winreg.KEY_SET_VALUE
)
winreg.SetValueEx(key, "AutoRecorder", 0, winreg.REG_SZ, command)
winreg.CloseKey(key)

print("[완료] 자동 시작 등록됨")
print(f"  {command}")
print("재부팅하면 자동으로 실행됩니다.")
