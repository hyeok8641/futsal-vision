import csv, cv2, numpy as np
from collections import defaultdict

OFF = 3000.0
CLIP = r"C:\futsal\clip_cam1_50min.mp4"
TIMES = [26.15, 26.35, 26.56, 26.70]
X0, Y0, W, H, Z = 920, 170, 600, 140, 2
FONT = cv2.FONT_HERSHEY_SIMPLEX

cand = defaultdict(list)
for r in csv.DictReader(open(r"C:\futsal\clip50_raw_merged.csv")):
    if r["conf"] != "":
        cand[float(r["t"])].append(tuple(float(r[k]) for k in ("x1", "y1", "x2", "y2", "conf")))
trk = {float(r["t"]): r for r in csv.DictReader(open(r"C:\futsal\clip50_track_merged.csv"))}

def near(d, ct):
    k = min(d, key=lambda x: abs(x - (OFF + ct)))
    return k if abs(k - (OFF + ct)) <= 0.02 else None

P = lambda x, y: (int((x - X0) * Z), int((y - Y0) * Z))
cap = cv2.VideoCapture(CLIP)
tiles = []
for ct in TIMES:
    cap.set(cv2.CAP_PROP_POS_MSEC, ct * 1000)
    ok, fr = cap.read()
    if not ok:
        continue
    tile = cv2.resize(fr[Y0:Y0 + H, X0:X0 + W], None, fx=Z, fy=Z, interpolation=cv2.INTER_NEAREST)
    k = near(cand, ct)
    for x1, y1, x2, y2, c in (cand[k] if k is not None else []):
        u = (x1 + x2) / 2
        name, col = ("A", (255, 0, 255)) if abs(u - 1000) <= 12 else (("B", (255, 255, 0)) if 1430 <= u <= 1500 else ("?", (200, 200, 200)))
        cv2.rectangle(tile, P(x1 - 4, y1 - 4), P(x2 + 4, y2 + 4), col, 1)
        cv2.putText(tile, f"{name} {c:.2f}", P(x1 - 4, y1 - 8), FONT, 0.6, col, 2)
    kt = near(trk, ct)
    st = trk[kt]["status"] if kt is not None else "none"
    if kt is not None and st != "missing":
        r = trk[kt]
        x1, y1, x2, y2 = (float(r[q]) for q in ("x1", "y1", "x2", "y2"))
        cv2.rectangle(tile, P(x1 - 8, y1 - 8), P(x2 + 8, y2 + 8), (0, 255, 255) if st == "detected" else (0, 165, 255), 2)
    cv2.putText(tile, f"{ct:.2f}s  track:{st}", (8, 24), FONT, 0.8, (255, 255, 255), 2)
    tiles.append(tile)
cap.release()
cv2.imwrite(r"C:\futsal\ab_2626.jpg", np.vstack(tiles))
print("저장: C:\\futsal\\ab_2626.jpg")
