import csv, sys
from collections import Counter

t0, t1 = float(sys.argv[1]) + 2700, float(sys.argv[2]) + 2700

raw = {}
for r in csv.DictReader(open(r"C:\futsal\clip_raw.csv")):
    t = float(r["t"])
    if t0 <= t <= t1:
        raw.setdefault(t, [])
        if r["conf"] != "":
            raw[t].append(float(r["conf"]))

def load(p):
    d = {}
    for r in csv.DictReader(open(p)):
        t = float(r["t"])
        if t0 <= t <= t1:
            d[t] = r["status"]
    return d

v1 = load(r"C:\futsal\clip_track.csv")
v2 = load(r"C:\futsal\clip_track_v2.csv")
ts = sorted(raw)
allc = [c for t in ts for c in raw[t]]

print(f"구간 {t0 - 2700:.1f}~{t1 - 2700:.1f}초, 프레임 {len(ts)}개, 후보가 있는 프레임 {sum(1 for t in ts if raw[t])}개")
if allc:
    print(f"후보 신뢰도: 최대 {max(allc):.2f} / 0.25 이상 {sum(c >= 0.25 for c in allc)}개 / 0.5 이상 {sum(c >= 0.5 for c in allc)}개")
else:
    print("후보 신뢰도: 후보 없음")
print("v1 상태:", dict(Counter(v1.values())))
print("v2 상태:", dict(Counter(v2.values())))
print("\n시각(클립)  후보수  최대신뢰도  v1  v2")
for t in ts[::3]:
    c = raw[t]
    print(f"{t - 2700:7.2f}  {len(c):4d}  {max(c) if c else 0:8.2f}  {v1.get(t, '-'):9s} {v2.get(t, '-')}")
