import csv
OFF = 3000.0
EV = [19.667, 20.833, 26.264, 30.562, 31.742, 41.164, 47.708]

def load(p):
    d = {}
    for r in csv.DictReader(open(p)):
        d.setdefault(float(r["t"]), [])
        if r["conf"] != "":
            d[float(r["t"])].append(float(r["conf"]))
    return d

for name, p in (("1280", r"C:\futsal\clip50_raw_r2.csv"), ("1920", r"C:\futsal\clip50_raw_1920.csv")):
    d = load(p)
    ts = sorted(d)
    n25 = sum(1 for t in ts if any(c >= .25 for c in d[t]))
    n10 = sum(1 for t in ts if d[t])
    boxes = sum(len(d[t]) for t in ts)
    print(f"[{name}] 프레임 {len(ts)}  후보>=0.25 프레임 {n25}  후보>=0.1 프레임 {n10}  후보 박스 합계 {boxes}")
    row = []
    for e in EV:
        w = [t for t in ts if abs(t - (OFF + e)) <= 0.4]
        row.append(f"{e:.1f}초:{sum(1 for t in w if any(c >= .25 for c in d[t]))}/{len(w)}")
    print("   구간별 (후보>=0.25 프레임/전체):", "  ".join(row))
