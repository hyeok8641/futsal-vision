import csv
import numpy as np

trk = list(csv.DictReader(open(r"C:\futsal\clip_track_v2.csv")))
crt = list(csv.DictReader(open(r"C:\futsal\clip_court_v2.csv")))
assert len(trk) == len(crt)

runs, cur = [], []
for a, b in zip(trk, crt):
    far = b["x_m"] != "" and float(b["x_m"]) > 20 and a["status"] == "detected"
    if far and (not cur or float(a["t"]) - cur[-1][0] <= 0.1):
        cur.append((float(a["t"]), float(a["conf"]), float(b["x_m"]), float(b["y_m"]), float(b["u"]), float(b["v"])))
    else:
        if cur:
            runs.append(cur)
        cur = [(float(a["t"]), float(a["conf"]), float(b["x_m"]), float(b["y_m"]), float(b["u"]), float(b["v"]))] if far else []
if cur:
    runs.append(cur)

print(f"cam1 x>20 검출 구간 {len(runs)}개 (클립 초 / 프레임 / 신뢰도 중앙값, 최소~최대 / 화면 이동 합 / 화면 속도)")
for g in runs:
    t = [p[0] - 2700 for p in g]
    c = np.array([p[1] for p in g])
    move = sum(np.hypot(g[i + 1][4] - g[i][4], g[i + 1][5] - g[i][5]) for i in range(len(g) - 1))
    span = max(t[-1] - t[0], 1 / 30)
    tag = ""
    if t[0] <= 49.7 and t[-1] >= 49.5:
        tag = "  <= 정상 공(확인)"
    if t[-1] >= 52.6 and t[0] <= 53.2:
        tag = "  <= 신발(확인)"
    print(f"  {t[0]:5.1f}~{t[-1]:5.1f}초  {len(g):3d}프레임  conf {np.median(c):.2f} ({c.min():.2f}~{c.max():.2f})  "
          f"{move:6.0f}px  {move / span:5.0f}px/s{tag}")
