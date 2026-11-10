import csv, cv2, numpy as np
from collections import defaultdict
from statistics import median

OFF = 2400.0
CLIP = r"C:\futsal\clip_cam1_40min.mp4"
load = lambda p: {float(r["t"]): r for r in csv.DictReader(open(p))}
old, new = load(r"C:\futsal\clip40_track_v2.csv"), load(r"C:\futsal\clip40n_track.csv")
ts = sorted(old)
isdet = lambda d, t: d.get(t, {}).get("status") == "detected"

def runs(sel):
    out, cur = [], []
    for t in sel:
        if cur and t - cur[-1] > 0.1:
            out.append(cur); cur = []
        cur.append(t)
    if cur:
        out.append(cur)
    return sorted(out, key=lambda g: -len(g))

lost = runs([t for t in ts if isdet(old, t) and not isdet(new, t)])
gain = runs([t for t in ts if isdet(new, t) and not isdet(old, t)])
remain = runs([t for t in ts if isdet(new, t) and (37.9 <= t - OFF <= 38.5 or 41.3 <= t - OFF <= 42.3)])

cap = cv2.VideoCapture(CLIP)
def sheet(title, rs, src, path, k=6):
    print(f"\n[{title}] 구간 {len(rs)}개, 프레임 {sum(len(g) for g in rs)}개")
    tiles = []
    for g in rs[:k]:
        mid = g[len(g) // 2]
        r = src[mid]
        confs = [float(src[t]["conf"]) for t in g if src[t]["conf"]]
        print(f"  {g[0]-OFF:6.2f}~{g[-1]-OFF:6.2f}초  {len(g):3d}프레임  conf 중앙값 {median(confs):.2f}")
        cap.set(cv2.CAP_PROP_POS_MSEC, (mid - OFF) * 1000)
        ok, fr = cap.read()
        if not ok:
            continue
        x1, y1, x2, y2 = (float(r[q]) for q in ("x1", "y1", "x2", "y2"))
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        cv2.rectangle(fr, (int(x1) - 6, int(y1) - 6), (int(x2) + 6, int(y2) + 6), (0, 255, 255), 1)
        X0 = int(min(max(0, cx - 100), 1920 - 200)); Y0 = int(min(max(0, cy - 70), 1080 - 140))
        t = cv2.resize(fr[Y0:Y0 + 140, X0:X0 + 200], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
        cv2.putText(t, f"{mid-OFF:.2f}s conf {float(r['conf']):.2f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        tiles.append(t)
    if tiles:
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        cv2.imwrite(path, np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))
        print("  저장:", path)

sheet("남아 있는 오검출 구간(새 모델 검출)", remain, new, r"C:\futsal\m2_remain.jpg", 4)
sheet("이전에만 검출 (잃은 것)", lost, old, r"C:\futsal\m2_lost.jpg", 6)
sheet("새 모델에서만 검출 (얻은 것)", gain, new, r"C:\futsal\m2_gain.jpg", 6)
cap.release()
