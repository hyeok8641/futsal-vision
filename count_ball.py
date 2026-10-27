from ultralytics import YOLO

model = YOLO("yolo26m.pt")
results = model.predict(
    source="test_1min.mp4",
    classes=[32],        # sports ball
    conf=0.1,
    imgsz=1280,
    device=0,
    stream=True,
    save=False
)

total = detected = 0
for r in results:
    total += 1
    if len(r.boxes) > 0:
        detected += 1

print(f"전체 프레임: {total}")
print(f"공 검출 프레임: {detected}")
print(f"검출 비율: {detected / total * 100:.1f}%")