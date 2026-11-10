import csv, sys
sys.path.insert(0, r"C:\futsal\court_repo")
from court_map import load, pixel_to_court

T0, T1 = 2708.0, 2710.6
cal2 = load(2, out_dir=r"C:\futsal\court_repo\out")

c1 = [r for r in csv.DictReader(open(r"C:\futsal\clip_court_v2.csv"))
      if r["x_m"] != "" and r["status"] == "detected"]
before = [r for r in c1 if float(r["t"]) < T0]
after = [r for r in c1 if float(r["t"]) > T1]
print("[cam1 기준]")
if before:
    r = before[-1]; print(f"  직전 검출 t={float(r['t'])-2700:.2f}초  코트 ({r['x_m']}, {r['y_m']}) m")
if after:
    r = after[0]; print(f"  직후 검출 t={float(r['t'])-2700:.2f}초  코트 ({r['x_m']}, {r['y_m']}) m")

rows = [r for r in csv.DictReader(open(r"C:\futsal\clip_cam2_raw.csv"))
        if r["conf"] != "" and T0 <= float(r["t"]) <= T1]
px = [[(float(r["x1"]) + float(r["x2"])) / 2, (float(r["y1"]) + float(r["y2"])) / 2] for r in rows]
xy = pixel_to_court(cal2, px, t=[float(r["t"]) for r in rows])

print("\n[cam2 후보]  시각(초)  신뢰도   화면(u,v)       코트(x,y) m")
for k in range(0, len(rows), 2):
    r = rows[k]
    print(f"  {float(r['t'])-2700:6.2f}   {float(r['conf']):.2f}   ({px[k][0]:6.0f},{px[k][1]:5.0f})   ({xy[k][0]:6.1f},{xy[k][1]:6.1f})")
