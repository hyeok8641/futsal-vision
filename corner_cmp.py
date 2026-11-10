import os
from ultralytics import YOLO
SRC = r"C:\futsal\ball_dataset\to_label"
names = ["000082","000084","000089","000101","000111","000123","000126","000134","000147",
         "000164","000169","000172","000193","000204","000207","000210"]
for tag in ("ball_v1_s", "ball_v2_s"):
    m = YOLO(rf"C:\futsal\runs\detect\{tag}\weights\best.pt")
    corner = total = 0
    for n in names:
        r = m.predict(source=os.path.join(SRC, f"cam1_t{n}.00.jpg"), imgsz=1280, device=0, conf=0.25, verbose=False)[0]
        for b in r.boxes.xyxy.tolist():
            total += 1
            corner += (b[0] + b[2]) / 2 > 1850 and (b[1] + b[3]) / 2 < 40
    print(f"{tag}: 모서리 사진 16장에서 검출 {total}개 중 모서리 {corner}개")
