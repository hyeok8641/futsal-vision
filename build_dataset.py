import os, shutil, yaml

SRC = r"C:\futsal\ball_dataset\to_label"
LAB = r"C:\futsal\ball_dataset\sam3_filtered\labels"
OUT = r"C:\futsal\ball_dataset\yolo"

for sp in ("train", "val"):
    for kind in ("images", "labels"):
        d = os.path.join(OUT, kind, sp)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

files = sorted(f for f in os.listdir(SRC)
               if f.lower().endswith(".jpg")
               and os.path.exists(os.path.join(LAB, os.path.splitext(f)[0] + ".txt")))

counts = {"train": 0, "val": 0}
for cam in ("cam1", "cam2"):
    fs = [f for f in files if f.startswith(cam + "_")]
    cut = int(len(fs) * 0.8)
    for i, f in enumerate(fs):
        sp = "train" if i < cut else "val"
        stem = os.path.splitext(f)[0]
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, "images", sp, f))
        shutil.copy(os.path.join(LAB, stem + ".txt"), os.path.join(OUT, "labels", sp, stem + ".txt"))
        counts[sp] += 1

data = {"path": OUT.replace("\\", "/"), "train": "images/train", "val": "images/val", "names": {0: "ball"}}
with open(os.path.join(OUT, "data.yaml"), "w") as f:
    yaml.safe_dump(data, f)
print("train", counts["train"], "장 / val", counts["val"], "장")
