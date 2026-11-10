import os, cv2, numpy as np
SRC = r"C:\futsal\ball_dataset\to_label"
LAB = r"C:\futsal\ball_dataset\sam3_filtered\labels"

hits, total = [], 0
for f in sorted(os.listdir(LAB)):
    for line in open(os.path.join(LAB, f)):
        p = line.split()
        if len(p) < 5:
            continue
        total += 1
        cx, cy, w, h = (float(v) for v in p[1:5])
        if cx * 1920 > 1850 and cy * 1080 < 40:
            hits.append((f, round(cx * 1920), round(cy * 1080), round(w * 1920), round(h * 1080)))
print(f"SAM3 라벨 파일 {len(os.listdir(LAB))}개, 박스 {total}개 중 오른쪽 위 모서리(x>1850, y<40)에 있는 라벨: {len(hits)}개")
for h in hits[:15]:
    print("  ", h)

corner = ["cam1_t000123.00.jpg", "cam1_t000204.00.jpg", "cam1_t000210.00.jpg", "cam1_t000111.00.jpg",
          "cam1_t000169.00.jpg", "cam1_t000193.00.jpg"]
control = ["cam1_t001596.00.jpg", "cam1_t002037.00.jpg"]
tiles = []
for name in corner + control:
    img = cv2.imread(os.path.join(SRC, name))
    if img is None:
        continue
    tile = cv2.resize(img[0:70, 1800:1920], None, fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
    if name in corner:
        cv2.rectangle(tile, (92 * 5, 0), (105 * 5, 9 * 5), (0, 255, 0), 1)
    cv2.putText(tile, name[4:15] + (" corner" if name in corner else " ctrl"), (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    tiles.append(tile)
while len(tiles) % 4:
    tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(r"C:\futsal\corner_crops.jpg", np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]))
print("저장: C:\\futsal\\corner_crops.jpg  (초록 사각형 = 오검출 위치, ctrl = 비교용 다른 시각)")
