import csv, sys, bisect, cv2

clip, track_csv, out_path, offset = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
PAD = 4
rows = list(csv.DictReader(open(track_csv)))
ts = [float(r["t"]) for r in rows]

cap = cv2.VideoCapture(clip)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
vw = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
i = 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    t = offset + i / fps
    j = bisect.bisect_left(ts, t)
    ks = [k for k in (j - 1, j) if 0 <= k < len(ts)]
    k = min(ks, key=lambda k: abs(ts[k] - t))
    r = rows[k]
    if abs(ts[k] - t) <= 0.04 and r["status"] != "missing":
        x1, y1, x2, y2 = (int(float(r[c])) for c in ("x1", "y1", "x2", "y2"))
        color = (0, 255, 0) if r["status"] == "detected" else (0, 165, 255)
        cv2.rectangle(fr, (x1 - PAD, y1 - PAD), (x2 + PAD, y2 + PAD), color, 2)
    vw.write(fr)
    i += 1
cap.release()
vw.release()
print("saved:", out_path)
