"""
자동 카메라 녹화 스크립트
config.json에 설정된 시각에 지정 카메라로 동영상을 촬영하여 저장합니다.
"""

import json
import os
import time
import schedule
import cv2
from datetime import datetime
from pathlib import Path


def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def next_sequence_number(save_folder: Path) -> int:
    """저장 폴더 내 기존 파일의 순번 중 최대값 + 1 반환"""
    existing = [
        f.name for f in save_folder.glob("*.mp4")
        if f.name[:3].isdigit()
    ]
    if not existing:
        return 1
    return max(int(name[:3]) for name in existing) + 1


def record_video(camera_index: int, save_folder: Path, duration_seconds: int):
    now = datetime.now()
    seq = next_sequence_number(save_folder)
    filename = f"{seq:03d}_{now.strftime('%y%m%d_%H%M')}.mp4"
    filepath = save_folder / filename

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[오류] 카메라 {camera_index}번을 열 수 없습니다.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(filepath), fourcc, fps, (width, height))

    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 녹화 시작 → {filepath}")

    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            print("[경고] 프레임을 읽지 못했습니다. 녹화를 중단합니다.")
            break
        writer.write(frame)

    cap.release()
    writer.release()
    print(f"[완료] 저장: {filepath}")


def main():
    config = load_config()

    camera_index    = config["camera_index"]
    save_folder     = Path(config["save_folder"])
    duration        = config["duration_seconds"]
    schedule_times  = config["schedule_times"]

    save_folder.mkdir(parents=True, exist_ok=True)

    def job():
        record_video(camera_index, save_folder, duration)

    for t in schedule_times:
        schedule.every().day.at(t).do(job)
        print(f"스케줄 등록: 매일 {t}")

    print("녹화 스케줄러 실행 중... (Ctrl+C로 종료)")
    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
