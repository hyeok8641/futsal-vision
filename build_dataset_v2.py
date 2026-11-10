import os, shutil, yaml, cv2, numpy as np
from ultralytics import YOLO

SRC = r"C:\futsal\ball_dataset\to_label"
OLD = r"C:\futsal\ball_dataset\yolo"
NEW = r"C:\futsal\ball_dataset\yolo_v2"
WEIGHTS = r"C:\futsal\runs\detect\ball_v1_s\weights\best.pt"

pos = ["cam1_t000210.00.jpg", "cam1_t000147.00.jpg", "cam1_t000273.00.jpg", "cam1_t001596.00.jpg"]
neg = [f"cam1_t{n}.00.jpg" for n in ("000082", "000089", "000101", "000123", "000126", "000134",
                                      "000164", "000169", "000172", "000193", "000204", "000207")]

shutil.rmtree(NEW, ignore_errors=True)
shutil.copytree(OLD, NEW, ignore=shutil.ignore_patterns("*.cache", "data.yaml"))
tr_img, tr_lab = os.path.join(NEW, "images", "train"), os.path.join(NEW, "labels", "train")
t_of = lambda n: float(n.split("_t")[1][:-4])
val_min = min(t_of(f) for f in os.listdir(os.path.join(NEW, "images", "val")) if f.startswith("cam1_"))
print(f"기존 cam1 검증 사진 중 가장 이른 시각: {val_min:.0f}초 (새 사진이 이보다 이르면 겹치지 않아요)")

model = YOLO(WEIGHTS)
tiles = []
for f in pos:
    img = cv2.imread(os.path.join(SRC, f))
    r = model.predict(source=img, imgsz=1280, device=0, conf=0.25, verbose=False)[0]
    boxes = [(c, b) for c, b in zip(r.boxes.conf.tolist(), r.boxes.xyxy.tolist())
             if not ((b[0] + b[2]) / 2 > 1850 and (b[1] + b[3]) / 2 < 40) and c >= 0.4]
    print(f"[양성] {f} (t={t_of(f):.0f}초): 사용할 박스 {len(boxes)}개 " + " ".join(f"{c:.2f}" for c, _ in boxes))
    shutil.copy(os.path.join(SRC, f), os.path.join(tr_img, f))
    with open(os.path.join(tr_lab, f[:-4] + ".txt"), "w") as lf:
        for c, (x1, y1, x2, y2) in boxes:
            lf.write(f"0 {(x1+x2)/2/1920:.6f} {(y1+y2)/2/1080:.6f} {(x2-x1)/1920:.6f} {(y2-y1)/1080:.6f}\n")
    for c, (x1, y1, x2, y2) in boxes:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        X0 = int(min(max(0, cx - 40), 1920 - 80)); Y0 = int(min(max(0, cy - 40), 1080 - 80))
        t = cv2.resize(img[Y0:Y0 + 80, X0:X0 + 80], None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST)
        cv2.rectangle(t, (int((x1 - X0) * 6), int((y1 - Y0) * 6)), (int((x2 - X0) * 6), int((y2 - Y0) * 6)), (0, 255, 0), 1)
        cv2.putText(t, f"{f[4:11]} {c:.2f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        tiles.append(t)

for f in neg:
    shutil.copy(os.path.join(SRC, f), os.path.join(tr_img, f))
    open(os.path.join(tr_lab, f[:-4] + ".txt"), "w").close()

yaml.safe_dump({"path": NEW.replace("\\", "/"), "train": "images/train", "val": "images/val", "names": {0: "ball"}},
               open(os.path.join(NEW, "data.yaml"), "w"))
print("학습 사진", len(os.listdir(tr_img)), "장 / 검증 사진", len(os.listdir(os.path.join(NEW, "images", "val"))), "장")
if tiles:
    cv2.imwrite(r"C:\futsal\pos_check.jpg", np.hstack(tiles[:4]))
    print("저장: C:\\futsal\\pos_check.jpg (초록 박스가 공에 맞는지 확인)")
