from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo26s.pt")
    model.train(
        data=r"C:\futsal\ball_dataset\yolo_v2\data.yaml",
        epochs=100,
        imgsz=1280,
        batch=4,
        device=0,
        patience=30,
        scale=0.3,
        degrees=0,
        name="ball_v2_s",
    )
