import csv
from collections import defaultdict
OFF = 3000.0
cand = defaultdict(list)
for r in csv.DictReader(open(r"C:\futsal\clip50_raw_merged.csv")):
    if r["conf"] != "":
        x1, y1, x2, y2, c = (float(r[k]) for k in ("x1", "y1", "x2", "y2", "conf"))
        cand[float(r["t"])].append((c, (x1 + x2) / 2, (y1 + y2) / 2))
load = lambda p: {float(r["t"]): r for r in csv.DictReader(open(p))}
a = load(r"C:\futsal\clip50_track_merged.csv")
b = load(r"C:\futsal\clip50_track_merged_v5.csv")

def d(r):
    if r["status"] == "missing":
        return "missing          "
    u, v = (float(r["x1"]) + float(r["x2"])) / 2, (float(r["y1"]) + float(r["y2"])) / 2
    return f"{r['status'][:4]} t{r['track_id']:>2} ({u:4.0f},{v:3.0f})"

print("클립초   v2                    v5                   | 후보(>=0.25): 신뢰도@(u,v)")
for t in sorted(a):
    ct = t - OFF
    if 41.8 <= ct <= 42.5:
        cs = " ".join(f"{c:.2f}@({u:.0f},{v:.0f})" for c, u, v in sorted(cand.get(t, []), reverse=True) if c >= 0.25)
        print(f"{ct:7.3f}  {d(a[t])}  {d(b[t])} | {cs if cs else '-'}")
