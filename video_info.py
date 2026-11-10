import sys
import cv2

for path in sys.argv[1:]:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(path, "→ 영상을 못 열었어요")
        continue
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(path)
    print("  해상도:", w, "x", h)
    print("  fps:", round(fps, 3))
    print("  총 프레임:", frames)
    print("  길이:", round(frames / fps / 60, 1), "분")
    cap.release()