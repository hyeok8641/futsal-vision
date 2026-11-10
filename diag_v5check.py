import csv, cv2, numpy as np
from collections import defaultdict

OFF = 3000.0
CLIP = r"C:\futsal\clip_cam1_50min.mp4"
TIMES = [26.85, 41.98, 42.38]
FONT = cv2.FONT_HERSHEY_SIMPLEX

cand = defaultdict(list)
for r in csv.DictReader(open(r"C:\futsal\clip50_raw_merged.csv")):
    if r["conf"] != "":
        cand[float(r["t"])].append(tuple(float(r[k]) for k in ("x1", "y1", "x2", "y2", "conf")))
load = lambda p: {float(r["t"]): r for r in csv.DictReader(open(p))}
a = load(r"C:\futsal\clip50_track_merged.csv")
b = load(r"C:\futsal\clip50_track_merged_v5.csv")

def key(d, ct):
    k = min(d, key=lambda x: abs(x - (OFF + ct)))
    return k if abs(k - (OFF + ct)) <= 0.02 else None

def box(r):
    return tuple(float(r[q]) for q in ("x1", "y1", "x2", "y2"))

cap = cv2.VideoCapture(CLIP)
tiles = []
for ct in TIMES:
    ka, kb = key(a, ct), key(b, ct)
    ra, rb = a.get(ka), b.get(kb)
    ref = ra if ra and ra["status"] != "missing" else (rb if rb and rb["status"] != "missing" else None)
    if ref is None:
        print(f"[{ct}초] 두 추적 모두 박스가 없어요")
        continue
    x1, y1, x2, y2 = box(ref)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    X0 = int(min(max(0, cx - 150), 1920 - 300)); Y0 = int(min(max(0, cy - 70), 1080 - 140)); Z = 3
    P = lambda x, y: (int((x - X0) * Z), int((y - Y0) * Z))
    cap.set(cv2.CAP_PROP_POS_MSEC, ct * 1000)
    ok, fr = cap.read()
    if not ok:
        continue
    tile = cv2.resize(fr[Y0:Y0 + 140, X0:X0 + 300], None, fx=Z, fy=Z, interpolation=cv2.INTER_NEAREST)
    kc = key(cand, ct)
    for c in (cand[kc] if kc is not None else []):
        if c[4] >= 0.25:
            cv2.rectangle(tile, P(c[0] - 3, c[1] - 3), P(c[2] + 3, c[3] + 3), (0, 255, 0), 1)
            cv2.putText(tile, f"{c[4]:.2f}", P(c[0] - 3, c[1] - 6), FONT, 0.5, (0, 255, 0), 1)
    for name, r, col, pad in (("v2", ra, (0, 255, 255), 8), ("v5", rb, (255, 0, 255), 12)):
        if r and r["status"] != "missing":
            bx = box(r)
            cv2.rectangle(tile, P(bx[0] - pad, bx[1] - pad), P(bx[2] + pad, bx[3] + pad), col, 2)
    sa = ra["status"] if ra else "none"; sb = rb["status"] if rb else "none"
    cv2.putText(tile, f"{ct:.2f}s  v2:{sa}  v5:{sb}", (8, 26), FONT, 0.7, (255, 255, 255), 2)
    tiles.append(tile)
    print(f"[{ct}초] v2={sa}, v5={sb}")
cap.release()
cv2.imwrite(r"C:\futsal\v5_check.jpg", np.vstack(tiles))
print("저장: C:\\futsal\\v5_check.jpg")
