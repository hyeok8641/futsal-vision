import sys
import numpy as np
import cv2

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

cal2 = load(2, out_dir=r"C:\futsal\court_repo\out")
cap = cv2.VideoCapture(r"C:\futsal\clip_cam2_45min.mp4")

us, vs = np.meshgrid(np.arange(0, 1920, 4), np.arange(0, 1080, 4))
grid = np.stack([us.ravel(), vs.ravel()], axis=1).astype(float)

targets = [("normal_4950", 49.61, 22.5, 4.1),
           ("unknown_5161", 51.61, 21.5, 9.5),
           ("shoe_5271", 52.71, 21.9, 11.9)]

for name, clip_t, x, y in targets:
    xy = pixel_to_court(cal2, grid, t=2700 + clip_t)
    d = np.hypot(xy[:, 0] - x, xy[:, 1] - y)
    d[np.isnan(d)] = np.inf
    k = int(np.argmin(d))
    u, v = int(grid[k, 0]), int(grid[k, 1])
    inside = d[k] < 1.5
    print(f"[{name}] 클립 {clip_t}초, cam1 좌표 ({x},{y}) m -> cam2 화면 u={u}, v={v}, 가장 가까운 격자까지 {d[k]:.2f} m "
          f"{'(화면 안)' if inside else '(화면 안에 이 좌표가 없음)'}")
    cap.set(cv2.CAP_PROP_POS_MSEC, clip_t * 1000)
    ok, fr = cap.read()
    if not ok:
        continue
    if inside:
        x0, y0 = max(0, u - 150), max(0, v - 100)
        crop = cv2.resize(fr[y0:y0 + 200, x0:x0 + 300], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        cv2.circle(crop, ((u - x0) * 3, (v - y0) * 3), 60, (0, 255, 0), 2)
        cv2.imwrite(rf"C:\futsal\cam2_chk_{name}.jpg", crop)
    else:
        cv2.imwrite(rf"C:\futsal\cam2_chk_{name}.jpg", cv2.resize(fr, (960, 540)))
cap.release()
print("저장: C:\\futsal\\cam2_chk_normal_4950.jpg / _unknown_5161.jpg / _shoe_5271.jpg")
