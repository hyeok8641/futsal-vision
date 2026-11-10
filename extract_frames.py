import cv2, os, sys

# 사용법: python extract_frames.py 영상경로 이름표 시작분 끝분 간격초
# 예:     python extract_frames.py videos/cam1.mp4 cam1 0 35 1
path, tag = sys.argv[1], sys.argv[2]
start_min, end_min, every_sec = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
OUT_DIR = "ball_dataset/images_all"
os.makedirs(OUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(path)
t = start_min * 60
saved = 0
while t < end_min * 60:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)   # 해당 시각으로 이동
    ok, frame = cap.read()
    if not ok:
        break
    cv2.imwrite(f"{OUT_DIR}/{tag}_t{t:09.2f}.jpg", frame)
    saved += 1
    t += every_sec
cap.release()
print(tag, "저장:", saved, "장")