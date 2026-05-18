import cv2

print("카메라 탐색 중...")
found = []

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"  [{i}] 카메라 발견 - {w}x{h}")
        found.append(i)
    cap.release()

if not found:
    print("  연결된 카메라가 없습니다.")
else:
    print(f"\n사용하려면 config.json의 camera_index를 위 번호로 설정하세요.")
