import csv, sys

def hotspots(path, name, radius=8, min_conf=0.25):
    dets = []
    for r in csv.DictReader(open(path)):
        if r["conf"] == "" or float(r["conf"]) < min_conf:
            continue
        u = (float(r["x1"]) + float(r["x2"])) / 2
        v = (float(r["y1"]) + float(r["y2"])) / 2
        dets.append((float(r["t"]) - 2700, u, v, float(r["conf"])))
    dets.sort(key=lambda d: -d[3])
    spots = []   # [u, v, 프레임 시각 집합]
    for t, u, v, c in dets:
        for s in spots:
            if abs(u - s[0]) <= radius and abs(v - s[1]) <= radius:
                s[2].add(round(t, 3)); break
        else:
            spots.append([u, v, {round(t, 3)}])
    spots.sort(key=lambda s: -len(s[2]))
    print(f"\n[{name}] 같은 자리(±{radius}px)에 반복해서 나온 후보 상위 6개")
    for u, v, ts in [(s[0], s[1], s[2]) for s in spots[:6]]:
        print(f"  화면({u:6.0f},{v:5.0f})  {len(ts):4d}프레임  클립 {min(ts):5.1f}~{max(ts):5.1f}초")

hotspots(r"C:\futsal\clip_raw.csv", "cam1")
hotspots(r"C:\futsal\clip_cam2_raw.csv", "cam2")
