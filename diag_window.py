import csv, sys
from collections import defaultdict

p, t0, t1 = sys.argv[1], float(sys.argv[2]) + 2700, float(sys.argv[3]) + 2700
by = defaultdict(list)
for r in csv.DictReader(open(p)):
    t = float(r["t"])
    if t0 <= t <= t1:
        by[t]
        if r["conf"] != "":
            by[t].append(float(r["conf"]))
ts = sorted(by)
has = [t for t in ts if by[t]]
allc = [c for t in ts for c in by[t]]
print(f"구간 {t0-2700:.1f}~{t1-2700:.1f}초: 프레임 {len(ts)}개, 후보가 있는 프레임 {len(has)}개")
if allc:
    print(f"후보 신뢰도: 최대 {max(allc):.2f} / 0.5 이상 {sum(c >= 0.5 for c in allc)}개 / 0.25 이상 {sum(c >= 0.25 for c in allc)}개")
for t in ts[::6]:
    c = by[t]
    print(f"  {t-2700:6.2f}초  후보 {len(c)}개  최대 {max(c) if c else 0:.2f}")
