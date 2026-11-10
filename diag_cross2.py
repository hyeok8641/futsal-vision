import csv, sys
import numpy as np

sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

cal2 = load(2, out_dir=r"C:\futsal\court_repo\out")
c2 = [r for r in csv.DictReader(open(r"C:\futsal\clip_cam2_raw_ns.csv")) if r["conf"] != ""]
t2 = np.array([float(r["t"]) for r in c2])
cf = np.array([float(r["conf"]) for r in c2])
px = np.array([[(float(r["x1"]) + float(r["x2"])) / 2, float(r["y2"])] for r in c2])
xy2 = pixel_to_court(cal2, px, t=t2)

pts = [r for r in csv.DictReader(open(r"C:\futsal\clip_court_v2.csv"))
       if r["status"] == "detected" and r["x_m"] != ""]

def window(name, a, b):
    print(f"\n[{name}] cam1 검출 → 같은 시각 cam2 후보 중 가장 가까운 것")
    shown = 0
    for r in pts:
        t = float(r["t"]) - 2700
        if not a <= t <= b:
            continue
        x, y = float(r["x_m"]), float(r["y_m"])
        m = np.abs(t2 - float(r["t"])) <= 0.02
        if not m.any():
            line = "cam2 후보 없음"
        else:
            d = np.hypot(xy2[m, 0] - x, xy2[m, 1] - y)
            k = int(np.nanargmin(d))
            idx = np.where(m)[0][k]
            line = (f"cam2 후보 {int(m.sum())}개, 최근접 {d[k]:.1f} m  "
                    f"(신뢰도 {cf[idx]:.2f}, 화면 u={px[idx][0]:.0f} v={px[idx][1]:.0f}, 코트 {xy2[idx][0]:.1f},{xy2[idx][1]:.1f})")
        if shown % 3 == 0:
            print(f"  {t:6.2f}초  cam1 코트({x:5.1f},{y:5.1f})  {line}")
        shown += 1

window("0:49.5~49.7 정상 공", 49.5, 49.7)
window("0:51.4~52.0 미확인", 51.4, 52.0)
window("0:52.6~53.2 신발", 52.6, 53.2)
