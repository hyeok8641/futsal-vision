import csv
import numpy as np
from collections import Counter

def run(path, name):
    rows = list(csv.DictReader(open(path)))
    pts = [r for r in rows if r["x_m"] != ""]
    out = lambda r: abs(float(r["x_m"])) > 21 or abs(float(r["y_m"])) > 11
    print(f"\n===== {name} =====")
    print("코트 밖 점의 상태:", dict(Counter(r["status"] for r in pts if out(r))))

    runs, cur = [], []
    for r in pts:
        if out(r) and (not cur or float(r["t"]) - float(cur[-1]["t"]) <= 0.1):
            cur.append(r)
        else:
            if cur:
                runs.append(cur)
            cur = [r] if out(r) else []
    if cur:
        runs.append(cur)
    runs.sort(key=lambda g: -len(g))
    print(f"코트 밖 구간 {len(runs)}개 (긴 순서 상위 8개)")
    for g in runs[:8]:
        xs = [float(r["x_m"]) for r in g]
        ys = [float(r["y_m"]) for r in g]
        st = dict(Counter(r["status"] for r in g))
        print(f"  클립 {float(g[0]['t'])-2700:5.1f}~{float(g[-1]['t'])-2700:5.1f}초  {len(g):3d}프레임  {st}  x {min(xs):.1f}~{max(xs):.1f}  y {min(ys):.1f}~{max(ys):.1f}")

    sp = []
    for a, b in zip(pts[:-1], pts[1:]):
        if a["status"] == "detected" and b["status"] == "detected" and a["track_id"] == b["track_id"]:
            dt = float(b["t"]) - float(a["t"])
            if 0 < dt < 0.2:
                d = np.hypot(float(b["x_m"]) - float(a["x_m"]), float(b["y_m"]) - float(a["y_m"]))
                sp.append((d / dt, float(b["t"]) - 2700, d))
    if sp:
        v = np.array([s[0] for s in sp])
        print(f"검출끼리 속도: 쌍 {len(sp)}개, 중앙값 {np.median(v):.1f} m/s, 최대 {v.max():.1f} m/s, 30 m/s 초과 {int((v > 30).sum())}개")
        for s in sorted(sp, key=lambda s: -s[0])[:3]:
            print(f"    클립 {s[1]:.2f}초  1프레임에 {s[2]:.1f} m 이동 ({s[0]:.0f} m/s)")

run(r"C:\futsal\clip_court_v2.csv", "cam1")
run(r"C:\futsal\clip_cam2_court.csv", "cam2")
