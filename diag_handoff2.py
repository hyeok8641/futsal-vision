import csv
from collections import defaultdict

raw = defaultdict(list)
for r in csv.DictReader(open(r"C:\futsal\clip_raw.csv")):
    if r["conf"] != "" and float(r["conf"]) >= 0.25:
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        raw[round(float(r["t"]), 4)].append((float(r["conf"]), (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1))

print("클립초  상태      트랙  신뢰도  중심(u,v)      크기     | 같은 프레임의 모든 후보 (신뢰도@(u,v) 크기)")
for r in csv.DictReader(open(r"C:\futsal\clip_track_v2.csv")):
    t = float(r["t"])
    ct = t - 2700
    if not 51.70 <= ct <= 52.75:
        continue
    if r["status"] == "missing":
        me = f"{ct:6.2f}  missing"
    else:
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        conf = r["conf"] if r["conf"] else "  -  "
        me = f"{ct:6.2f}  {r['status']:9s} {r['track_id']:>3}  {conf:>6}  ({(x1+x2)/2:5.0f},{(y1+y2)/2:4.0f})  {x2-x1:3.0f}x{y2-y1:<3.0f}"
    cs = " ".join(f"{c:.2f}@({u:.0f},{v:.0f}) {w:.0f}x{h:.0f}" for c, u, v, w, h in sorted(raw.get(round(t, 4), []), reverse=True))
    print(f"{me:62s}| {cs}")
