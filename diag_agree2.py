import csv, sys
import numpy as np

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

OUT = r"C:\futsal\court_repo\out"
cal1, cal2 = load(1, out_dir=OUT), load(2, out_dir=OUT)

def read(p):
    rows = [r for r in csv.DictReader(open(p)) if r["status"] == "detected"]
    cols = [np.array([float(r[k]) for r in rows]) for k in ("t", "x1", "y1", "x2", "y2")]
    return cols

a = read(r"C:\futsal\clip_track_v2.csv")
b = read(r"C:\futsal\clip_cam2_track.csv")

pairs = []
for i, t in enumerate(a[0]):
    j = int(np.searchsorted(b[0], t))
    c = [k for k in (j - 1, j) if 0 <= k < len(b[0])]
    if not c:
        continue
    k = min(c, key=lambda k: abs(b[0][k] - t))
    if abs(b[0][k] - t) <= 0.02:
        pairs.append((i, k))
ia, ib = np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])

def coords(cal, d, idx, mode):
    x1, y1, x2, y2 = d[1][idx], d[2][idx], d[3][idx], d[4][idx]
    u = (x1 + x2) / 2
    v = (y1 + y2) / 2 if mode == "center" else y2
    return pixel_to_court(cal, np.stack([u, v], 1), t=d[0][idx])

for mode, name in (("center", "박스 중심"), ("bottom", "박스 아래 중앙")):
    ca, cb = coords(cal1, a, ia, mode), coords(cal2, b, ib, mode)
    ok = ~(np.isnan(ca).any(1) | np.isnan(cb).any(1))
    diff = ca[ok] - cb[ok]
    d = np.hypot(diff[:, 0], diff[:, 1])
    mid = (np.abs(ca[ok][:, 0]) <= 15) & (np.abs(cb[ok][:, 0]) <= 15)
    print(f"[{name}] 쌍 {int(ok.sum())}개 | 거리 중앙값 {np.median(d):.2f} m | "
          f"1m 이내 {np.mean(d < 1) * 100:.0f}% / 2m 이내 {np.mean(d < 2) * 100:.0f}% / 3m 이내 {np.mean(d < 3) * 100:.0f}%")
    print(f"    평균 어긋남(cam1-cam2): dx={diff[:, 0].mean():+.2f} m, dy={diff[:, 1].mean():+.2f} m  "
          f"(중앙값 dx={np.median(diff[:, 0]):+.2f}, dy={np.median(diff[:, 1]):+.2f})")
    if mid.any():
        print(f"    중앙(|x|<=15) {int(mid.sum())}쌍: 거리 중앙값 {np.median(d[mid]):.2f} m, 2m 이내 {np.mean(d[mid] < 2) * 100:.0f}%")
