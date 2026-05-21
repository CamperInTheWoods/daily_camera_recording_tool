"""
자동 카메라 녹화 스크립트
config.json에 설정된 시각에 지정 카메라로 동영상을 촬영하여 저장합니다.

사용법:
  python recorder.py                        -- 스케줄 모드
  python recorder.py --preview              -- 프리뷰 창 (R: 녹화, S: 중단, Q: 종료)
  python recorder.py --config               -- 현재 설정 확인
  python recorder.py --camera 1             -- 카메라 번호 변경
  python recorder.py --time 09:00 18:00     -- 촬영 시각 변경
  python recorder.py --duration 120         -- 촬영 길이(초) 변경
"""

import sys
import json
import time
import threading
import schedule
import cv2
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"


def normalize_time(t: str) -> str:
    if ":" not in t and len(t) == 4:
        return f"{t[:2]}:{t[2:]}"
    return t


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)
    config["schedule_times"] = [normalize_time(t) for t in config["schedule_times"]]
    return config


def save_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def parse_args():
    args = sys.argv[1:]
    result = {}

    if "--config" in args:
        result["show_config"] = True
    if "--preview" in args:
        result["preview"] = True
    if "--camera" in args:
        i = args.index("--camera")
        result["camera_index"] = int(args[i + 1])
    if "--duration" in args:
        i = args.index("--duration")
        result["duration_seconds"] = int(args[i + 1])
    if "--time" in args:
        i = args.index("--time")
        times = []
        for v in args[i + 1:]:
            if v.startswith("--"):
                break
            if ":" not in v and len(v) == 4:
                v = f"{v[:2]}:{v[2:]}"
            times.append(v)
        result["schedule_times"] = times

    return result


def next_sequence_number(save_folder: Path) -> int:
    existing = [
        f.name for f in save_folder.glob("*.mp4")
        if f.name[:3].isdigit()
    ]
    if not existing:
        return 1
    return max(int(name[:3]) for name in existing) + 1


def make_writer(save_folder: Path, cap: cv2.VideoCapture):
    now = datetime.now()
    seq = next_sequence_number(save_folder)
    filename = f"{seq:03d}_{now.strftime('%y%m%d_%H%M')}.mp4"
    filepath = save_folder / filename

    fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(str(filepath), fourcc, fps, (width, height))
    print(f"[녹화 시작] {filepath}")
    return writer, filepath


def preview_mode(camera_index: int, save_folder: Path):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[오류] 카메라 {camera_index}번을 열 수 없습니다.")
        return

    writer = None
    filepath = None
    recording = False

    print("프리뷰 실행 중 | R: 녹화 시작  S: 녹화 중단  Q: 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[경고] 프레임을 읽지 못했습니다.")
            break

        if recording and writer:
            writer.write(frame)
            cv2.putText(frame, "REC", (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        cv2.imshow("Camera Preview", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') or key == ord('R'):
            if not recording:
                writer, filepath = make_writer(save_folder, cap)
                recording = True
        elif key == ord('s') or key == ord('S'):
            if recording and writer:
                writer.release()
                print(f"[녹화 중단] 저장: {filepath}")
                writer = None
                recording = False
        elif key == ord('q') or key == ord('Q'):
            break
        elif cv2.getWindowProperty("Camera Preview", cv2.WND_PROP_VISIBLE) < 1:
            break

    if recording and writer:
        writer.release()
        print(f"[녹화 중단] 저장: {filepath}")

    cap.release()
    cv2.destroyAllWindows()


def record_video(camera_index: int, save_folder: Path, duration_seconds: int):
    now = datetime.now()
    seq = next_sequence_number(save_folder)
    filename = f"{seq:03d}_{now.strftime('%y%m%d_%H%M')}.mp4"
    filepath = save_folder / filename

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[오류] 카메라 {camera_index}번을 열 수 없습니다.")
        return

    fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0
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


def schedule_mode(camera_index: int, save_folder: Path, duration: int, schedule_times: list):
    def job():
        t = threading.Thread(target=record_video, args=(camera_index, save_folder, duration))
        t.daemon = True
        t.start()

    for t in schedule_times:
        schedule.every().day.at(t).do(job)
        print(f"스케줄 등록: 매일 {t}")

    print("녹화 스케줄러 실행 중... (Ctrl+C로 종료)")
    while True:
        schedule.run_pending()
        time.sleep(10)


def main():
    args   = parse_args()
    config = load_config()

    # 인자로 넘어온 값은 config에 덮어쓰고 저장
    changed = False
    for key in ("camera_index", "duration_seconds", "schedule_times"):
        if key in args:
            config[key] = args[key]
            changed = True
    if changed:
        save_config(config)
        print("설정 저장됨")

    if args.get("show_config"):
        print("[ 현재 설정 ]")
        print(f"  camera_index     : {config['camera_index']}")
        print(f"  save_folder      : {config['save_folder']}")
        print(f"  duration_seconds : {config['duration_seconds']}초")
        print(f"  schedule_times   : {', '.join(config['schedule_times'])}")
        return

    camera_index   = config["camera_index"]
    save_folder    = Path(config["save_folder"])
    duration       = config["duration_seconds"]
    schedule_times = config["schedule_times"]

    save_folder.mkdir(parents=True, exist_ok=True)

    if args.get("preview"):
        preview_mode(camera_index, save_folder)
    else:
        schedule_mode(camera_index, save_folder, duration, schedule_times)


if __name__ == "__main__":
    main()
