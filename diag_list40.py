import csv
from collections import defaultdict
OFF = 2400.0
rows = list(csv.DictReader(open(r"C:\futsal\clip40_track_v2.csv")))
dt = (float(rows[-1]["t"]) - float(rows[0]["t"])) / (len(rows) - 1)

def runs(status):
    out, cur = [], None
    for r in rows:
        t = float(r["t"])
        if r["status"] == status:
            cur = [t, t] if cur is None else [cur[0], t]
        elif cur:
            out.append(cur); cur = None
    if cur:
        out.append(cur)
    return sorted(out, key=lambda g: -(g[1] - g[0]))

for st in ("missing", "predicted"):
    print(f"\n[{st}] 긴 구간 상위 6개 (재생 시간 = 클립 초)")
    for a, b in runs(st)[:6]:
        print(f"  {a - OFF:6.2f} ~ {b - OFF:6.2f}초  ({(b - a) / dt + 1:.0f}프레임)")

tr = defaultdict(list)
for r in rows:
    if r["status"] == "detected":
        tr[r["track_id"]].append(float(r["t"]))
print("\n[궤적] 번호  시작~끝(초)  검출 프레임")
for k, v in sorted(tr.items(), key=lambda kv: kv[1][0]):
    print(f"  {k:>3}  {v[0] - OFF:6.2f} ~ {v[-1] - OFF:6.2f}  {len(v)}")

print("\n[의심 점프] 같은 궤적의 연속 검출 사이 중심이 80px 넘게 이동")
prev = None
for r in rows:
    if r["status"] != "detected":
        prev = None
        continue
    c = ((float(r["x1"]) + float(r["x2"])) / 2, (float(r["y1"]) + float(r["y2"])) / 2)
    if prev and prev[0] == r["track_id"] and float(r["t"]) - prev[2] < 0.1:
        d = ((c[0] - prev[1][0]) ** 2 + (c[1] - prev[1][1]) ** 2) ** 0.5
        if d > 80:
            print(f"  {float(r['t']) - OFF:6.2f}초  {d:.0f}px 이동")
    prev = (r["track_id"], c, float(r["t"]))
