import csv
OFF = 3000.0
EV = [(19.667, "가림"), (20.833, "공중"), (26.264, "불명"), (30.562, "불명"), (31.742, "불명"), (41.164, "공중"), (47.708, "공중+신발")]
load = lambda p: {float(r["t"]): r["status"] for r in csv.DictReader(open(p))}
v = {"1280": load(r"C:\futsal\clip50_track_v2_r2.csv"),
     "1920": load(r"C:\futsal\clip50_track_v2_1920.csv"),
     "합침": load(r"C:\futsal\clip50_track_merged.csv")}
ts = sorted(v["1280"])
print("재생시간  구간       " + "          ".join(v) + "   (±0.4초 24프레임 중 검출/예측/없음)")
for pb, lab in EV:
    w = [t for t in ts if abs(t - (OFF + pb)) <= 0.4]
    cells = []
    for k in v:
        s = [v[k][t] for t in w]
        cells.append(f"{s.count('detected'):2d}/{s.count('predicted'):2d}/{s.count('missing'):2d}")
    print(f"{pb:7.3f} {lab:8s}  " + "      ".join(cells))
