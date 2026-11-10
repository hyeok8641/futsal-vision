import csv, cv2, numpy as np
from collections import defaultdict

OFF = 3000.0
CLIP = r"C:\futsal\clip_cam1_50min.mp4"
TIMES = [25.95, 26.15, 26.35, 26.56]
FONT = cv2.FONT_HERSHEY_SIMPLEX

def load_raw(p):
    d = defaultdict(list)
    for r in csv.DictReader(open(p)):
        if r["conf"] != "":
            d[float(r["t"])].append(tuple(float(r[k]) for k in ("x1", "y1", "x2", "y2", "conf")))
    return d

raw1280 = load_raw(r"C:\futsal\clip50_raw_r2.csv")
raw1920 = load_raw(r"C:\futsal\clip50_raw_1920.csv")
trk = {float(r["t"]): r for r in csv.DictReader(open(r"C:\futsal\clip50_track_merged.csv"))}

def near(d, t):
    k = min(d, key=lambda x: abs(x - (OFF + t)))
    return k if abs(k - (OFF + t)) <= 0.02 else None

def at(d, t):
    k = near(d, t)
    return d[k] if k is not None else []

cs = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
      for d in (raw1280, raw1920) for k in d if OFF + 25.7 <= k <= OFF + 26.8 for b in d[k]]
cx, cy = (float(np.median([c[0] for c in cs])), float(np.median([c[1] for c in cs]))) if cs else (960.0, 540.0)
X0 = int(min(max(0, cx - 180), 1920 - 360)); Y0 = int(min(max(0, cy - 100), 1080 - 200)); Z = 3
print(f"확대 영역 중심 약 ({cx:.0f},{cy:.0f}), 구간 25.7~26.8초 후보 {len(cs)}개")

cap = cv2.VideoCapture(CLIP)
tiles = []
for t in TIMES:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        continue
    tile = cv2.resize(fr[Y0:Y0 + 200, X0:X0 + 360], None, fx=Z, fy=Z, interpolation=cv2.INTER_NEAREST)
    P = lambda x, y: (int((x - X0) * Z), int((y - Y0) * Z))
    line = {}
    for name, d, col, dy in (("1280", raw1280, (0, 255, 0), -5), ("1920", raw1920, (255, 255, 0), 22)):
        items = []
        for b in at(d, t):
            if b[4] < 0.1:
                continue
            cv2.rectangle(tile, P(b[0] - 3, b[1] - 3), P(b[2] + 3, b[3] + 3), col, 1)
            lab = P(b[0] - 3, b[1] - 3 if dy < 0 else b[3] + 3)
            cv2.putText(tile, f"{b[4]:.2f}", (lab[0], lab[1] + (dy if dy < 0 else 14)), FONT, 0.5, col, 1)
            items.append(f"{b[4]:.2f}@({(b[0]+b[2])/2:.0f},{(b[1]+b[3])/2:.0f})")
        line[name] = " ".join(items) if items else "없음"
    k = near(trk, t)
    st = "없음"
    if k is not None:
        r = trk[k]
        st = r["status"]
        if st != "missing":
            x1, y1, x2, y2 = (float(r[q]) for q in ("x1", "y1", "x2", "y2"))
            col = (0, 255, 255) if st == "detected" else (0, 165, 255)
            cv2.rectangle(tile, P(x1 - 7, y1 - 7), P(x2 + 7, y2 + 7), col, 2)
    cv2.putText(tile, f"{t:.2f}s  track:{st}", (8, 26), FONT, 0.8, (255, 255, 255), 2)
    print(f"[{t:.2f}초] 추적={st}\n   1280 후보: {line['1280']}\n   1920 후보: {line['1920']}")
    tiles.append(tile)
cap.release()
rows = [np.hstack(tiles[i:i + 2]) for i in range(0, len(tiles) - 1, 2)]
cv2.imwrite(r"C:\futsal\cand_2626.jpg", np.vstack(rows))
print("저장: C:\\futsal\\cand_2626.jpg")
