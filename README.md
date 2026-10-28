# 풋살 영상 분석 - 객체 인식 (선수·공)

풋살 경기 영상에서 선수(person)와 공(sports ball)을 찾는 객체 인식 파트입니다.
모델은 YOLO26(Ultralytics)을 사용합니다.

## 환경

- Python 3.12
- NVIDIA GPU 권장 (CUDA 12.6 기준 테스트)
- Ultralytics (YOLO26)

## 설치

가상환경을 만들고, PyTorch(GPU 버전)를 **먼저** 설치한 뒤 ultralytics를 설치합니다.

```bash
py -3.12 -m venv venv
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -U ultralytics
```

GPU 인식 확인:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

`True`가 나와야 합니다. GPU가 없으면 `pip install -U ultralytics`만 해도 되지만 매우 느립니다.

## 파일 설명

| 파일 | 설명 |
|---|---|
| `detect_person.py` | 선수(person) 감지·추적 (YOLO26m + ByteTrack) |
| `baseline_ball.py` | 학습 전 공 검출 baseline (sports ball 클래스) |
| `count_ball.py` | 공이 검출된 프레임 비율 계산 |
| `video_info.py` | 영상 해상도, fps, 총 프레임 확인 |

## 실행 방법

1. 영상 파일(예: `test_1min.mp4`)을 코드와 같은 폴더에 둡니다. 영상은 용량과 개인정보 문제로 GitHub에 올리지 않았고, 별도로 전달합니다.
2. 같은 폴더에서 실행합니다.

```bash
python detect_person.py
python baseline_ball.py
python count_ball.py
```

3. 결과는 `runs/` 폴더에 저장됩니다.

모델 파일(`yolo26m.pt`)은 처음 실행할 때 자동으로 다운로드됩니다.

## 공 인식 baseline (학습 전)

- 조건: YOLO26m 사전학습 모델, 클래스 sports ball, conf=0.1, imgsz=1280
- 결과: 1분 영상 3,528프레임 중 1,945프레임(55.1%)에서 공 후보 검출
- 참고: 정답 라벨과 비교한 값이 아니라 검출 프레임 비율이라 오검출이 포함될 수 있습니다.

## 공 인식 학습 계획

1. 두 카메라 영상에서 프레임 추출 (800~1,500장)
2. Roboflow로 `ball` 클래스 라벨링
3. YOLO26m 파인튜닝 (imgsz=1280)
4. 학습에 쓰지 않은 구간으로 Precision, Recall, mAP50 평가
5. 목표: Recall 0.6 이상, mAP50 0.5 이상

## GitHub에 올리지 않는 파일

영상(`*.mp4`), 모델(`*.pt`), 결과(`runs/`), 가상환경(`venv/`), 데이터셋(`ball_dataset/`)은 용량·개인정보 문제로 `.gitignore`로 제외했습니다.
학습 후 공 모델(`best.pt`)은 구글 드라이브로 별도 공유합니다.
