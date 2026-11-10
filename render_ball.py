from ultralytics import YOLO

CLIP = r"C:\futsal\clip_45min.mp4"
MODEL = r"C:\futsal\runs\detect\ball_v1_s\weights\best.pt"

YOLO(MODEL).predict(
    source=CLIP,
    imgsz=1280,
    device=0,
    conf=0.25,
    show_labels=False,   # "ball" 글자 숨김
    show_conf=False,     # 0.xx 숫자 숨김
    line_width=2,        # 박스 선 두께
    save=True,
    project=r"C:\futsal\runs\detect",
    name="clip45_boxonly",
    verbose=False,
)
print("saved: C:\\futsal\\runs\\detect\\clip45_boxonly")
