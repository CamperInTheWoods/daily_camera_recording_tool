# Auto Camera Recorder

지정한 시각에 자동으로 카메라 영상을 촬영하여 저장하는 Python 스크립트입니다.

## 요구사항

- Python 3.8 이상
- 연결된 카메라 (USB 웹캠 등)

## 다른 컴퓨터에서 처음 실행할 때

```
1. 이 폴더를 복사
2. setup.bat 실행  ← 패키지 설치
3. config.json 설정 수정
4. python recorder.py 실행
```

### 컴퓨터 시작 시 자동 실행 (선택)

```
register_startup.bat 실행
```

Windows 시작 프로그램에 등록됩니다. 로그인 후 백그라운드에서 자동 실행됩니다.

---

## config.json 설정

| 항목 | 설명 | 예시 |
|------|------|------|
| `camera_index` | 카메라 번호 (0부터 시작) | `0` |
| `save_folder` | 저장 폴더 경로 | `"C:/recordings"` |
| `duration_seconds` | 촬영 길이 (초) | `60` |
| `schedule_times` | 매일 촬영할 시각 목록 | `["09:00", "18:00"]` |

카메라가 여러 개인 경우 `camera_index`를 0, 1, 2... 순서로 바꿔가며 테스트하세요.

---

## 저장 파일명 형식

```
001_260518_0900.mp4
↑순번  ↑날짜  ↑시각
```

---

## 명령어 목록

| 명령어 | 설명 |
|--------|------|
| `python recorder.py` | 스케줄러 실행 |
| `python list_cameras.py` | 연결된 카메라 목록 확인 |
| `register_startup.bat` | 컴퓨터 시작 시 자동 실행 등록 (재부팅 후 적용) |
| `tasklist \| findstr pythonw` | 백그라운드에서 돌고 있는지 확인 |
| `taskkill /f /im pythonw.exe` | 백그라운드 프로세스 종료 |

스케줄러 수동 실행 종료: `Ctrl+C`
