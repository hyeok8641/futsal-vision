import csv
from collections import defaultdict
OFF = 3000.0
cand = defaultdict(list)
for r in csv.DictReader(open(r"C:\futsal\clip50_raw_merged.csv")):
    if r["conf"] != "":
        x1, y1, x2, y2, c = (float(r[k]) for k in ("x1", "y1", "x2", "y2", "conf"))
        cand[float(r["t"])].append((c, (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1))
trk = {float(r["t"]): r for r in csv.DictReader(open(r"C:\futsal\clip50_track_merged.csv"))}

print("클립초   추적상태      | 후보(신뢰도>=0.1, 높은 순): 신뢰도@(u,v) 크기")
for t in sorted(trk):
    ct = t - OFF
    if not 25.7 <= ct <= 26.8:
        continue
    r = trk[t]
    if r["status"] == "missing":
        me = "missing         "
    else:
        u, v = (float(r["x1"]) + float(r["x2"])) / 2, (float(r["y1"]) + float(r["y2"])) / 2
        me = f"{r['status'][:4]} t{r['track_id']:>2} ({u:.0f},{v:.0f})"
    cs = " ".join(f"{c:.2f}@({u:.0f},{v:.0f}) {w:.0f}x{h:.0f}"
                  for c, u, v, w, h in sorted(cand.get(t, []), reverse=True) if c >= 0.1)
    print(f"{ct:7.3f}  {me:18s}| {cs if cs else '없음'}")
