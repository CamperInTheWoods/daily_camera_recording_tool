==================================================
  Auto Camera Recorder
  지정 시각에 자동으로 카메라 영상을 촬영하여 저장
==================================================


[ 요구사항 ]

  - Python 3.8 이상
  - 연결된 카메라 (USB 웹캠 등)


[ 처음 설치 순서 ]

  1. setup.bat 실행          -- 패키지 설치
  2. config.json 수정        -- 카메라/시각/저장경로 설정
  3. register_startup.bat    -- 자동 시작 등록
  4. 재부팅                  -- 이후 자동으로 돌아감


[ config.json 설정 항목 ]

  camera_index      카메라 번호 (0부터 시작, 보통 0)
  save_folder       영상 저장 폴더 경로
  duration_seconds  촬영 길이 (초 단위)
  schedule_times    매일 촬영할 시각 목록


[ 저장 파일명 형식 ]

  001_260518_0900.mp4
  순번_날짜_시각


[ 명령어 목록 ]

  python recorder.py                  스케줄러 실행 (수동)
  python recorder.py --preview        카메라 프리뷰 창 띄우기 (R: 녹화, S: 중단, Q: 종료)
  python list_cameras.py              연결된 카메라 목록 확인
  register_startup.bat                자동 시작 등록 (재부팅 후 적용)
  tasklist | findstr pythonw          백그라운드 실행 중인지 확인
  taskkill /f /im pythonw.exe         백그라운드 프로세스 종료
  git pull                            최신 버전으로 업데이트

  수동 실행 종료: Ctrl+C
