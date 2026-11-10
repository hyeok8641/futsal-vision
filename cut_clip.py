import cv2, sys, os

src, dst, start_s, dur_s = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
if os.path.exists(dst):
    print("이미 있음:", dst); sys.exit()
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_MSEC, start_s * 1000)
w, h = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
for _ in range(int(fps * dur_s)):
    ok, fr = cap.read()
    if not ok: break
    out.write(fr)
out.release(); cap.release()
print("saved:", dst, f"fps={fps:.3f}")
