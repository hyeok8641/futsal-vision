import os, shutil
from ultralytics import YOLO

SRC = r"C:\futsal\ball_dataset\to_label"
LAB = r"C:\futsal\ball_dataset\sam3_filtered\labels"
OUT = r"C:\futsal\ball_dataset\neg_review"
WEIGHTS = r"C:\futsal\runs\detect\ball_v1_s\weights\best.pt"

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg"))
excluded = [f for f in files if not os.path.exists(os.path.join(LAB, os.path.splitext(f)[0] + ".txt"))]
print(f"to_label {len(files)}장 중 SAM3 라벨이 없어서 학습에서 빠진 사진 {len(excluded)}장")

model = YOLO(WEIGHTS)
hi = mid = none = 0
for f in excluded:
    r = model.predict(source=os.path.join(SRC, f), imgsz=1280, device=0, conf=0.25, verbose=False)[0]
    n = len(r.boxes)
    mx = float(r.boxes.conf.max()) if n else 0.0
    if n:
        r.save(filename=os.path.join(OUT, f"pred_{mx:.2f}_{f}"))
    if mx >= 0.5:
        hi += 1
    elif n:
        mid += 1
    else:
        none += 1
print(f"모델 예측: 신뢰도 0.5 이상 {hi}장 / 0.25~0.5 {mid}장 / 예측 없음 {none}장")
print("예측이 있는 사진만 저장했어요:", OUT)
