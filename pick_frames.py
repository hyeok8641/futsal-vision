import os, shutil, sys

# 사용법: python pick_frames.py 원본폴더 이름표 간격
# 예:     python pick_frames.py ball_dataset/images_all/cam1_train_0-35min cam1 21
src, tag, step = sys.argv[1], sys.argv[2], int(sys.argv[3])
dst = "ball_dataset/to_label"
os.makedirs(dst, exist_ok=True)

files = sorted(f for f in os.listdir(src) if f.endswith(".jpg"))
picked = files[::step]                       # step번째마다 1장
for f in picked:
    shutil.copy(os.path.join(src, f), os.path.join(dst, f))
print(tag, "원본", len(files), "장 중", len(picked), "장 복사")