import csv, cv2, numpy as np

CLIP = r"C:\futsal\clip_45min.mp4"
FONT = cv2.FONT_HERSHEY_SIMPLEX

def load(p):
    d = {}
    for r in csv.DictReader(open(p)):
        d[float(r["t"]) - 2700] = r
    return d

v2, v3 = load(r"C:\futsal\clip_track_v2.csv"), load(r"C:\futsal\clip_track_v3.csv")
raw = {}
for r in csv.DictReader(open(r"C:\futsal\clip_raw.csv")):
    if r["conf"] != "" and float(r["conf"]) >= 0.25:
        raw.setdefault(round(float(r["t"]) - 2700, 3), []).append(r)

keys = sorted(v2)
lost = [t for t in keys if 46.1 <= t <= 46.6 and v2[t]["status"] == "detected" and v3[t]["status"] != "detected"]
print("잃은 프레임:", len(lost), f"({lost[0]:.2f}~{lost[-1]:.2f}초)" if lost else "")
picks = [lost[0], lost[len(lost) // 2], lost[-1]] if lost else []
for t in (46.0, 46.6):
    picks.append(min(keys, key=lambda k: abs(k - t)))
picks = sorted(set(picks))[:6]

cap = cv2.VideoCapture(CLIP)
tiles = []
for t in picks:
    ref = v2[t]
    cx = (float(ref["x1"]) + float(ref["x2"])) / 2 if ref["status"] != "missing" else 1000
    cy = (float(ref["y1"]) + float(ref["y2"])) / 2 if ref["status"] != "missing" else 300
    X0, Y0 = int(max(0, cx - 100)), int(max(0, cy - 70))
    Z = 4
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000 + 2700 * 1000 * 0)
    ok, fr = cap.read()
    if not ok:
        continue
    row = []
    for name, v in (("v2", v2), ("v3", v3)):
        tile = cv2.resize(fr[Y0:Y0 + 140, X0:X0 + 200], None, fx=Z, fy=Z, interpolation=cv2.INTER_NEAREST)
        for r in raw.get(round(t, 3), []):
            x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
            cv2.rectangle(tile, (int((x1 - 3 - X0) * Z), int((y1 - 3 - Y0) * Z)), (int((x2 + 3 - X0) * Z), int((y2 + 3 - Y0) * Z)), (0, 255, 0), 1)
            cv2.putText(tile, f"{float(r['conf']):.2f}", (int((x1 - 3 - X0) * Z), int((y1 - 5 - Y0) * Z)), FONT, 0.5, (0, 255, 0), 1)
        r = v[t]
        if r["status"] != "missing":
            x1, y1, x2, y2 = (float(r[k]) for k in ("x1", "y1", "x2", "y2"))
            col = (0, 255, 255) if r["status"] == "detected" else (0, 165, 255)
            cv2.rectangle(tile, (int((x1 - 7 - X0) * Z), int((y1 - 7 - Y0) * Z)), (int((x2 + 7 - X0) * Z), int((y2 + 7 - Y0) * Z)), col, 2)
            cv2.putText(tile, f"trk{r['track_id']} {r['status'][:4]}", (int((x1 - 7 - X0) * Z), int((y2 + 17 - Y0) * Z)), FONT, 0.5, col, 1)
        cv2.putText(tile, f"{name} {t:.2f}s {r['status']}", (8, 24), FONT, 0.7, (255, 255, 255), 2)
        row.append(tile)
    tiles.append(np.hstack(row))
cap.release()

if not tiles:
    raise SystemExit("그릴 프레임이 없어요")
sheet = np.vstack(tiles)
cv2.imwrite(r"C:\futsal\diff_46.jpg", sheet)
print("저장: C:\\futsal\\diff_46.jpg", sheet.shape[1], "x", sheet.shape[0])
