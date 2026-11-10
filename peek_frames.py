import sys, cv2, numpy as np

# 사용법: python peek_frames.py 출력.jpg 시간1 시간2 ... (초)
out_path = sys.argv[1]
times = [float(x) for x in sys.argv[2:]]
VIDEOS = {1: r"C:\futsal\videos\cam1.mp4", 2: r"C:\futsal\videos\cam2.mp4"}

rows = []
for cam, path in VIDEOS.items():
    cap = cv2.VideoCapture(path)
    tiles = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if not ok:
            fr = np.zeros((1080, 1920, 3), np.uint8)
        fr = cv2.resize(fr, (640, 360))
        cv2.putText(fr, f"cam{cam}  {t:.0f}s", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        tiles.append(fr)
    cap.release()
    rows.append(np.hstack(tiles))

cv2.imwrite(out_path, np.vstack(rows))
print("saved:", out_path)
