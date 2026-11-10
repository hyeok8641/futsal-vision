import csv, sys
import numpy as np

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

cal2 = load(2, out_dir=r"C:\futsal\court_repo\out")
TOL_T, DIST, MINC = 0.02, 1.5, 0.25

c2 = [r for r in csv.DictReader(open(r"C:\futsal\clip_cam2_raw_ns.csv"))
      if r["conf"] != "" and float(r["conf"]) >= MINC]
t2 = np.array([float(r["t"]) for r in c2])
px = np.array([[(float(r["x1"]) + float(r["x2"])) / 2, float(r["y2"])] for r in c2])
xy2 = pixel_to_court(cal2, px, t=t2)
o = np.argsort(t2)
t2, xy2 = t2[o], xy2[o]

pts = [r for r in csv.DictReader(open(r"C:\futsal\clip_court_v2.csv"))
       if r["status"] == "detected" and r["x_m"] != ""]
res = []
for r in pts:
    t = float(r["t"])
    x, y = float(r["x_m"]), float(r["y_m"])
    lo, hi = np.searchsorted(t2, t - TOL_T), np.searchsorted(t2, t + TOL_T)
    ok = False
    if hi > lo:
        d = np.hypot(xy2[lo:hi, 0] - x, xy2[lo:hi, 1] - y)
        d = d[~np.isnan(d)]
        ok = bool(len(d) and d.min() <= DIST)
    res.append((t - 2700, x, y, ok))

def show(name, sel):
    n = len(sel)
    a = sum(1 for s in sel if s[3])
    print(f"{name}: {n}개 중 cam2 확인 {a}개 ({a / n * 100 if n else 0:.0f}%)")

show("cam1 전체 검출", res)
show("  x<=12 (cam1에 가까운 쪽)", [s for s in res if s[1] <= 12])
show("  x>12  (cam1에서 먼 쪽)", [s for s in res if s[1] > 12])
print()
show("0:49.5~49.7 (정상 인식으로 확인한 구간)", [s for s in res if 49.5 <= s[0] <= 49.7])
show("0:51.4~52.0 (미확인)", [s for s in res if 51.4 <= s[0] <= 52.0])
show("0:52.6~53.2 (신발 오검출 구간)", [s for s in res if 52.6 <= s[0] <= 53.2])
