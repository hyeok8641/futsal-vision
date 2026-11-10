import csv, bisect
import numpy as np

def load(p):
    d = []
    for r in csv.DictReader(open(p)):
        if r["status"] == "detected" and r["x_m"] != "":
            d.append((float(r["t"]), float(r["x_m"]), float(r["y_m"])))
    return d

a = load(r"C:\futsal\clip_court_v2.csv")       # cam1
b = load(r"C:\futsal\clip_cam2_court.csv")     # cam2
bt = [t for t, _, _ in b]
pairs = []
for t, x, y in a:
    j = bisect.bisect_left(bt, t)
    cand = [k for k in (j - 1, j) if 0 <= k < len(b)]
    if not cand:
        continue
    k = min(cand, key=lambda k: abs(bt[k] - t))
    if abs(bt[k] - t) <= 0.02:
        pairs.append((t - 2700, x, y, b[k][1], b[k][2], float(np.hypot(x - b[k][1], y - b[k][2]))))

print(f"cam1 검출 {len(a)}개, cam2 검출 {len(b)}개, 같은 시각에 둘 다 검출 {len(pairs)}쌍")
if pairs:
    d = np.array([p[5] for p in pairs])
    print(f"전체 거리: 중앙값 {np.median(d):.2f} m / 1m 이내 {np.mean(d<1)*100:.0f}% / 2m 이내 {np.mean(d<2)*100:.0f}% / 3m 이내 {np.mean(d<3)*100:.0f}%")
    mid = np.array([max(abs(p[1]), abs(p[3])) <= 15 for p in pairs])
    if mid.any():
        print(f"두 점 모두 |x|≤15m: {int(mid.sum())}쌍, 중앙값 {np.median(d[mid]):.2f} m, 2m 이내 {np.mean(d[mid]<2)*100:.0f}%")
    if (~mid).any():
        print(f"한쪽이라도 |x|>15m: {int((~mid).sum())}쌍, 중앙값 {np.median(d[~mid]):.2f} m, 2m 이내 {np.mean(d[~mid]<2)*100:.0f}%")
    print("\n가장 어긋난 10쌍 (클립 초 / cam1 좌표 / cam2 좌표 / 거리)")
    for t, x1, y1, x2, y2, dd in sorted(pairs, key=lambda p: -p[5])[:10]:
        print(f"  {t:6.2f}  ({x1:6.1f},{y1:5.1f})  ({x2:6.1f},{y2:5.1f})  {dd:5.1f} m")
