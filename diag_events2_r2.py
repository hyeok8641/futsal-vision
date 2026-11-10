import csv
from collections import Counter
OFF = 3000.0
EV = [(19.667, "가림"), (20.833, "공중"), (26.264, "불명"), (30.562, "불명"), (31.742, "불명"), (41.164, "공중"), (47.708, "공중+신발")]
RAW, V2, V4 = r"C:\futsal\clip50_raw_r2.csv", r"C:\futsal\clip50_track_v2_r2.csv", r"C:\futsal\clip50_track_v4_r2.csv"

raw = {}
for r in csv.DictReader(open(RAW)):
    raw.setdefault(float(r["t"]), [])
    if r["conf"] != "":
        raw[float(r["t"])].append(float(r["conf"]))
st = lambda p: {float(r["t"]): r["status"] for r in csv.DictReader(open(p))}
s2, s4 = st(V2), st(V4)
ts = sorted(raw)
print("재생시간  구간 프레임  후보>=0.25인 프레임  후보>=0.1인 프레임  최대신뢰도  v2 상태            v4 상태")
for pb, lab in EV:
    w = [t for t in ts if abs(t - (OFF + pb)) <= 0.4]
    mx = max((c for t in w for c in raw[t]), default=0)
    print(f"{pb:7.3f} {lab:7s} {len(w):3d}  {sum(1 for t in w if any(c >= .25 for c in raw[t])):3d}  "
          f"{sum(1 for t in w if raw[t]):3d}  {mx:.2f}  {dict(Counter(s2[t] for t in w))}  {dict(Counter(s4[t] for t in w))}")

for name, pre in (("31.742 근처", "3031.7"), ("47.708 근처", "3047.7")):
    print(f"\n[{name} 원본 줄]")
    for label, p in (("raw", RAW), ("v2 ", V2), ("v4 ", V4)):
        for line in open(p):
            if line.startswith(pre):
                print(" ", label, line.strip())

