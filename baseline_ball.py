from ultralytics import YOLO

model = YOLO("yolo26m.pt")
model.predict(
    source="test_1min.mp4",
    classes=[32],          # 32 = sports ball (공)
    conf=0.1,              # 공은 작아서 낮게
    imgsz=1280,
    device=0,
    save=True,
    project="runs/baseline",
    name="ball"
)