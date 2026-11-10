import csv
from collections import Counter
OFF = 2400.0
old = {float(r["t"]): r["status"] for r in csv.DictReader(open(r"C:\futsal\clip40_track_v2.csv"))}
new = {float(r["t"]): r["status"] for r in csv.DictReader(open(r"C:\futsal\clip40n_track.csv"))}
print("\n구간(재생 초)        이전(v1 모델)                      새 모델(v2)")
for name, a, b in (("오검출 37.5(바지)", 37.40, 37.65), ("오검출 38.2(신발)", 38.00, 38.40), ("오검출 41.5(신발)", 41.40, 42.20)):
    ks = [t for t in old if a <= t - OFF <= b]
    print(f"{name:14s} {str(dict(Counter(old[t] for t in ks))):34s} {dict(Counter(new.get(t, 'x') for t in ks))}")
lost = [t for t in old if old[t] == "detected" and new.get(t) != "detected"]
gain = [t for t in old if new.get(t) == "detected" and old[t] != "detected"]
print(f"\n이전에는 검출이었는데 새 모델에서는 아닌 프레임 {len(lost)}개 / 새로 검출 {len(gain)}개")
