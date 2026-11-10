import csv, cv2, numpy as np

CLIP = r"C:\futsal\clip_45min.mp4"
TIMES = [51.50, 51.78, 52.08, 52.41, 52.58, 52.71]
X0, X1, Y0, Y1, Z = 850, 1080, 150, 260, 4
FONT = cv2.FONT_HERSHEY_SIMPLEX

def load(path):
    d = {}
    for r in csv.DictReader(open(path)):
        d.setdefault(float(r["t"]) - 2700, []).append(r)
    return d

def near(d, t):
    k = min(d, key=lambda k: abs(k - t))
    return d[k] if abs(k - t) <= 0.02 else []

raw = load(r"C:\futsal\clip_raw.csv")
trk = load(r"C:\futsal\clip_track_v3.csv")
P = lambda x, y: (int((x - X0) * Z), int((y - Y0) * Z))

cap = cv2.VideoCapture(CLIP)
tiles = []
for t in TIMES:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        raise SystemExit(f"프레임을 못 읽었어요: {t}")
    tile = cv2.resize(fr[Y0:Y1, X0:X1], None, fx=Z, fy=Z, interpolation=cv2.INTER_NEAREST)
    for r in near(raw, t):
        if r["conf"] == "" or float(r["conf"]) < 0.25:
            continue
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        cv2.rectangle(tile, P(x1 - 3, y1 - 3), P(x2 + 3, y2 + 3), (0, 255, 0), 1)
        cv2.putText(tile, f"{float(r['conf']):.2f}", P(x1 - 3, y1 - 5), FONT, 0.5, (0, 255, 0), 1)
    for r in near(trk, t):
        if r["status"] == "missing":
            continue
        x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
        col = (0, 255, 255) if r["status"] == "detected" else (0, 165, 255)
        cv2.rectangle(tile, P(x1 - 7, y1 - 7), P(x2 + 7, y2 + 7), col, 2)
        cv2.putText(tile, f"trk{r['track_id']} {r['status'][:4]}", P(x1 - 7, y2 + 17), FONT, 0.5, col, 1)
    cv2.putText(tile, f"{t:.2f}s", (8, 24), FONT, 0.8, (255, 255, 255), 2)
    tiles.append(tile)
cap.release()

sheet = np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])])
cv2.imwrite(r"C:\futsal\handoff_view_v3.jpg", sheet)
print("저장: C:\\futsal\\handoff_view_v3.jpg", sheet.shape[1], "x", sheet.shape[0])

