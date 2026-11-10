import os, cv2, numpy as np
from ultralytics import YOLO

SRC = r"C:\futsal\ball_dataset\to_label"
LAB = r"C:\futsal\ball_dataset\sam3_filtered\labels"
WEIGHTS = r"C:\futsal\runs\detect\ball_v1_s\weights\best.pt"
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg")
               and not os.path.exists(os.path.join(LAB, os.path.splitext(f)[0] + ".txt")))
model = YOLO(WEIGHTS)

rows = []
for f in files:
    img = cv2.imread(os.path.join(SRC, f))
    r = model.predict(source=img, imgsz=1280, device=0, conf=0.25, verbose=False)[0]
    for b, c in zip(r.boxes.xyxy.tolist(), r.boxes.conf.tolist()):
        rows.append((f, c, b, img))
rows.sort(key=lambda x: -x[1])

print("순번  신뢰도  박스(x1,y1,x2,y2)           크기     위치   파일")
tiles, corner = [], 0
for i, (f, c, b, img) in enumerate(rows, 1):
    x1, y1, x2, y2 = b
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    tag = "오른쪽위" if cx > 1700 and cy < 100 else ""
    corner += bool(tag)
    print(f"{i:3d}   {c:.2f}   ({x1:6.0f},{y1:5.0f},{x2:6.0f},{y2:5.0f})  {x2-x1:3.0f}x{y2-y1:<3.0f}  {tag:6s} {f}")
    X0 = int(min(max(0, cx - 50), 1920 - 100)); Y0 = int(min(max(0, cy - 50), 1080 - 100))
    tile = cv2.resize(img[Y0:Y0 + 100, X0:X0 + 100], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
    cv2.rectangle(tile, (int((x1 - X0) * 4), int((y1 - Y0) * 4)), (int((x2 - X0) * 4), int((y2 - Y0) * 4)), (0, 255, 0), 1)
    cv2.putText(tile, f"{i} {c:.2f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    tiles.append(tile)
print(f"\n전체 {len(rows)}개 중 오른쪽 위 모서리(x>1700, y<100) {corner}개")
while len(tiles) % 5:
    tiles.append(np.zeros_like(tiles[0]))
sheet = np.vstack([np.hstack(tiles[i:i + 5]) for i in range(0, len(tiles), 5)])
cv2.imwrite(r"C:\futsal\neg_boxes.jpg", sheet)
print("저장: C:\\futsal\\neg_boxes.jpg (번호 = 위 표의 순번)")
