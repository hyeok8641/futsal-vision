import csv
OFF = 3000.0
EVENTS = [(19.667, "발에 가림"), (20.833, "공중"), (26.264, "원인 불명"), (30.562, "원인 불명"),
          (31.742, "원인 불명"), (41.164, "공중"), (47.708, "공중+신발")]

def load(p):
    return {float(r["t"]): r for r in csv.DictReader(open(p))}
v2, v4 = load(r"C:\futsal\clip50_track_v2.csv"), load(r"C:\futsal\clip50_track_v4.csv")
raw = {}
for r in csv.DictReader(open(r"C:\futsal\clip50_raw.csv")):
    if r["conf"] != "":
        raw.setdefault(float(r["t"]), []).append(r)
ts = sorted(v2)

def desc(r):
    if r["status"] == "missing":
        return "missing"
    u, v = (float(r["x1"]) + float(r["x2"])) / 2, (float(r["y1"]) + float(r["y2"])) / 2
    return f'{r["status"]} trk{r["track_id"]} ({u:.0f},{v:.0f})'

for pb, label in EVENTS:
    k = min(ts, key=lambda x: abs(x - (OFF + pb)))
    print(f"\n[{pb:.3f}초 · {label}]  가장 가까운 프레임 {k - OFF:.3f}초")
    print("  추적 v2:", desc(v2[k]), "| v4:", desc(v4[k]))
    for x in [t for t in ts if abs(t - k) <= 0.05]:
        cs = " ".join(
            f'{float(r["conf"]):.2f}@({(float(r["x1"]) + float(r["x2"])) / 2:.0f},{(float(r["y1"]) + float(r["y2"])) / 2:.0f}) '
            f'{float(r["x2"]) - float(r["x1"]):.0f}x{float(r["y2"]) - float(r["y1"]):.0f}'
            for r in sorted(raw.get(x, []), key=lambda r: -float(r["conf"])))
        print(f"    {x - OFF:7.3f}초 후보: {cs if cs else '없음'}")
