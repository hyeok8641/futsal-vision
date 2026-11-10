import os, cv2, numpy as np
SRC = r"C:\futsal\ball_dataset\to_label"
names = ["000082","000084","000089","000101","000111","000123","000126","000134","000147",
         "000164","000169","000172","000193","000204","000207","000210"]
tiles = []
for i, n in enumerate(names, 1):
    img = cv2.imread(os.path.join(SRC, f"cam1_t{n}.00.jpg"))
    if img is None:
        print("없음:", n)
        continue
    small = cv2.resize(img[170:420, 0:1920], (960, 125))
    big = cv2.resize(small, (1440, 187))
    cv2.putText(big, f"#{i} t{n}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    tiles.append(big)
for k in range(0, len(tiles), 4):
    cv2.imwrite(rf"C:\futsal\corner_full_{k // 4 + 1}.jpg", np.vstack(tiles[k:k + 4]))
print("저장:", [rf"C:\futsal\corner_full_{k // 4 + 1}.jpg" for k in range(0, len(tiles), 4)])
