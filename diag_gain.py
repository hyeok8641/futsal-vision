import csv, cv2, numpy as np
from statistics import median

OFF = 3000.0
CLIP = r"C:\futsal\clip_cam1_50min.mp4"
load = lambda p: {float(r["t"]): r for r in csv.DictReader(open(p))}
a = load(r"C:\futsal\clip50_track_v2_r2.csv")      # 1280
b = load(r"C:\futsal\clip50_track_v2_1920.csv")    # 1920
ts = sorted(a)
isdet = lambda d, t: d.get(t, {}).get("status") == "detected"
gained = [t for t in ts if isdet(b, t) and not isdet(a, t)]
lost = [t for t in ts if isdet(a, t) and not isdet(b, t)]

def runs(sel):
    out, cur = [], []
    for t in sel:
        if cur and t - cur[-1] > 0.1:
            out.append(cur); cur = []
        cur.append(t)
    if cur:
        out.append(cur)
    return sorted(out, key=lambda g: -len(g))

cap = cv2.VideoCapture(CLIP)
def sheet(title, rs, src, path):
    print(f"\n[{title}] 구간 {len(rs)}개, 프레임 {sum(len(g) for g in rs)}개 (긴 순서 상위 6개)")
    tiles = []
    for g in rs[:6]:
        mid = g[len(g) // 2]
        r = src[mid]
        conf = median(float(src[t]["conf"]) for t in g if src[t]["conf"])
        print(f"  {g[0]-OFF:6.2f}~{g[-1]-OFF:6.2f}초  {len(g):3d}프레임  conf 중앙값 {conf:.2f}")
        cap.set(cv2.CAP_PROP_POS_MSEC, (mid - OFF) * 1000)
        ok, fr = cap.read()
        if not ok:
            continue
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        cv2.rectangle(fr, (int(x1) - 6, int(y1) - 6), (int(x2) + 6, int(y2) + 6), (0, 255, 255), 1)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        X0 = int(min(max(0, cx - 100), 1920 - 200)); Y0 = int(min(max(0, cy - 70), 1080 - 140))
        tile = cv2.resize(fr[Y0:Y0 + 140, X0:X0 + 200], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
        cv2.putText(tile, f"{mid-OFF:.2f}s conf {float(r['conf']):.2f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        tiles.append(tile)
    if tiles:
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
        cv2.imwrite(path, np.vstack(rows))
        print("  저장:", path)

sheet("1920에서만 검출 (얻은 것)", runs(gained), b, r"C:\futsal\gained_1920.jpg")
sheet("1280에서만 검출 (잃은 것)", runs(lost), a, r"C:\futsal\lost_1920.jpg")
cap.release()
