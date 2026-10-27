import cv2

cap = cv2.VideoCapture("test_1min.mp4")
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("해상도:", w, "x", h)
print("fps:", fps)
print("총 프레임:", frames)
print("길이(초):", round(frames / fps, 1))
cap.release()