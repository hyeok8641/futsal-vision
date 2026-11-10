import csv, sys
import numpy as np
import cv2

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

CLIP_T = 9.0
T = 2700 + CLIP_T
cal2 = load(2, out_dir=r"C:\futsal\court_repo\out")

target = np.array([(-10.27 - 8.93) / 2, (3.96 + 4.05) / 2])
us, vs = np.meshgrid(np.arange(0, 1920, 2), np.arange(0, 1080, 2))
grid = np.stack([us.ravel(), vs.ravel()], axis=1).astype(float)
xy = pixel_to_court(cal2, grid, t=T)
d = np.hypot(xy[:, 0] - target[0], xy[:, 1] - target[1])
d[np.isnan(d)] = np.inf
k = int(np.argmin(d))
if not np.isfinite(d[k]):
    sys.exit("이 시각은 코트 변환이 안 되는 구간이에요")
u0, v0 = int(grid[k, 0]), int(grid[k, 1])
print(f"[1] cam1이 본 공 위치 ({target[0]:.1f}, {target[1]:.1f}) m 는 cam2 화면의 약 (u={u0}, v={v0}) (격자 오차 {d[k]:.2f} m)")

rows = [r for r in csv.DictReader(open(r"C:\futsal\clip_cam2_raw.csv")) if r["conf"] != ""]
for name, (cu, cvv, rad) in {"A": (1695, 92, 30), "B": (908, 31, 8)}.items():
    ts = set()
    for r in rows:
        x = (float(r["x1"]) + float(r["x2"])) / 2
        y = (float(r["y1"]) + float(r["y2"])) / 2
        if abs(x - cu) <= rad and abs(y - cvv) <= rad and float(r["conf"]) >= 0.25:
            ts.add(float(r["t"]) - 2700)
    if ts:
        print(f"[2] 후보 {name} (u={cu}, v={cvv}) 근처: 1800프레임 중 {len(ts)}프레임, 클립 {min(ts):.1f}~{max(ts):.1f}초에 걸쳐 나타남")
    else:
        print(f"[2] 후보 {name}: 없음")

cap = cv2.VideoCapture(r"C:\futsal\clip_cam2_45min.mp4")
cap.set(cv2.CAP_PROP_POS_MSEC, CLIP_T * 1000)
ok, clean = cap.read()
cap.release()
if not ok:
    sys.exit("프레임을 못 읽었어요")

fr = clean.copy()
for (cu, cvv, col, label) in [(u0, v0, (0, 255, 0), "pred"), (1695, 92, (0, 0, 255), "A"), (908, 31, (0, 255, 255), "B")]:
    cv2.circle(fr, (int(cu), int(cvv)), 28, col, 2)
    cv2.putText(fr, label, (int(cu) + 32, int(cvv)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, col, 2)
cv2.imwrite(r"C:\futsal\cam2_check.jpg", fr)

x0, y0 = max(0, u0 - 150), max(0, v0 - 100)
crop = cv2.resize(clean[y0:y0 + 200, x0:x0 + 300], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
cv2.circle(crop, ((u0 - x0) * 3, (v0 - y0) * 3), 90, (0, 255, 0), 2)
cv2.imwrite(r"C:\futsal\cam2_check_pred.jpg", crop)
print("저장: C:\\futsal\\cam2_check.jpg (전체, 후보 표시), C:\\futsal\\cam2_check_pred.jpg (예상 위치 확대)")
