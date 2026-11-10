import csv, sys
import numpy as np

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

OUT = r"C:\futsal\court_repo\out"
TOL_T, DIST, MINC = 0.02, 1.5, 0.25
BINS = [(-99, -20), (-20, -10), (-10, 0), (0, 10), (10, 20), (20, 99)]

def cands(path, cam):
    cal = load(cam, out_dir=OUT)
    rows = [r for r in csv.DictReader(open(path)) if r["conf"] != "" and float(r["conf"]) >= MINC]
    t = np.array([float(r["t"]) for r in rows])
    px = np.array([[(float(r["x1"]) + float(r["x2"])) / 2, float(r["y2"])] for r in rows])
    xy = pixel_to_court(cal, px, t=t)
    o = np.argsort(t)
    return t[o], xy[o]

def tracked(path):
    return [(float(r["t"]), float(r["x_m"]), float(r["y_m"]))
            for r in csv.DictReader(open(path)) if r["status"] == "detected" and r["x_m"] != ""]

def report(title, pts, ot, oxy):
    conf = []
    for t, x, y in pts:
        lo, hi = np.searchsorted(ot, t - TOL_T), np.searchsorted(ot, t + TOL_T)
        ok = False
        if hi > lo:
            d = np.hypot(oxy[lo:hi, 0] - x, oxy[lo:hi, 1] - y)
            d = d[~np.isnan(d)]
            ok = bool(len(d) and d.min() <= DIST)
        conf.append((x, ok))
    print(f"\n{title}")
    for a, b in BINS:
        sel = [ok for x, ok in conf if a <= x < b]
        label = f"x {a if a > -99 else '  '}~{b if b < 99 else '  '}"
        print(f"  {label:14s} 검출 {len(sel):4d}개  상대 카메라 확인 {sum(sel):4d}개 ({(sum(sel) / len(sel) * 100) if sel else 0:3.0f}%)")

c2t, c2xy = cands(r"C:\futsal\clip_cam2_raw_ns.csv", 2)
c1t, c1xy = cands(r"C:\futsal\clip_raw_ns.csv", 1)
report("[cam1 검출을 cam2가 확인하는 비율]", tracked(r"C:\futsal\clip_court_v2.csv"), c2t, c2xy)
report("[cam2 검출을 cam1이 확인하는 비율]", tracked(r"C:\futsal\clip_cam2_court.csv"), c1t, c1xy)
