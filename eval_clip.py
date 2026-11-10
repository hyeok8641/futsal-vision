import cv2, os
from ultralytics import YOLO

SRC = r"C:\futsal\videos\cam1.mp4"
CLIP = r"C:\futsal\clip_45min.mp4"
START_SEC, DUR_SEC = 45 * 60, 60

if not os.path.exists(CLIP):
    cap = cv2.VideoCapture(SRC)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_MSEC, START_SEC * 1000)
    w, h = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(CLIP, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    for _ in range(int(fps * DUR_SEC)):
        ok, fr = cap.read()
        if not ok: break
        out.write(fr)
    out.release(); cap.release()
    print("clip saved")

def count(model, **kw):
    total = one = multi = 0
    for r in model.predict(source=CLIP, stream=True, imgsz=1280, device=0, verbose=False, **kw):
        total += 1
        n = len(r.boxes)
        one += n >= 1
        multi += n >= 2
    return total, one, multi

t, a, m = count(YOLO("yolo26m.pt"), classes=[32], conf=0.1)
print(f"baseline  : frames={t}, detected={a} ({a/t*100:.1f}%), 2+ boxes={m}")

ft = YOLO(r"C:\futsal\runs\detect\ball_v1_s\weights\best.pt")
t, a, m = count(ft, conf=0.25)
print(f"finetuned : frames={t}, detected={a} ({a/t*100:.1f}%), 2+ boxes={m}")

ft.predict(source=CLIP, imgsz=1280, device=0, conf=0.25, save=True,
           project=r"C:\futsal\runs\detect", name="clip45_ft", verbose=False)
print("video saved: C:\\futsal\\runs\\detect\\clip45_ft")
