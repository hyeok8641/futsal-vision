# 풋살 영상 분석 - 공 인식·추적

두 카메라(cam1, cam2)로 찍은 풋살 경기 영상에서 공을 찾고 추적하는 파트입니다.
모델은 YOLO26s(Ultralytics)를 우리 영상으로 학습한 공 전용 모델(`best.pt`)을 씁니다.
팀 저장소(futsal-analytics/futsal-analytics)의 `ball-tracking` 브랜치에도 추적 코드가 올라가 있습니다.

## 환경

- Python 3.12, NVIDIA GPU 권장 (RTX 5060, torch 2.11+cu128에서 사용)
- ultralytics, opencv-python, numpy

```bash
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -m pip install -U ultralytics
```

## 추적 파이프라인

| 단계 | 파일 | 하는 일 |
|---|---|---|
| 1 | `detect_video2.py` | 영상에서 공 후보 찾기 (1280, 1920 두 해상도로 각각 실행) |
| 2 | `merge_raw.py` | 두 해상도 결과 합치기 (IoU 0.3) |
| 3 | `filter_static.py` | 한자리에 오래 있는 예비공 지우기 (cam2) |
| 4 | `track_ball.py` | 칼만 필터로 프레임마다 공 하나 고르기, 잠깐 안 보이면 예측 |
| 5 | `to_court.py` | 박스 아래 중앙점을 코트 좌표(m)로 변환 (팀원 court_map 사용) |
| - | `render_dual.py` | 두 카메라 추적 결과를 좌우로 붙인 확인용 영상 |

cam1(60fps)은 stride 2로 약 30fps, cam2(30fps)는 stride 1로 처리합니다. 모든 결과는 시간(초) 기준입니다.

## 모델 학습

| 파일 | 하는 일 |
|---|---|
| `extract_frames.py` | 영상에서 일정 간격으로 사진 뽑기 |
| `pick_frames.py` | 라벨링할 사진 고르기 |
| `build_dataset.py` | 학습/검증 데이터 나누기 (카메라별 시간순 80/20) |
| `train_ball.py` | YOLO26s 학습 |

라벨은 SAM3로 자동 생성했습니다 (SAM3 코드는 별도 환경에서 실행, 이 저장소에는 없음).

## 평가·도구

| 파일 | 하는 일 |
|---|---|
| `eval_labels.py` | 직접 눈으로 만든 정답 라벨로 끊김·오류 시간 집계 |
| `peek_frames.py` | 지정 시각의 두 카메라 장면을 jpg 격자로 |
| `cut_clip.py` | 영상에서 일부 구간 잘라내기 |
| `render_track.py` | 카메라 하나의 추적 결과 영상 |
| `video_info.py` | 영상 해상도, fps, 총 프레임 확인 |
| `report/` | 발표 PPT 생성 코드 |

## GitHub에 올리지 않는 파일

영상(`*.mp4`), 모델(`*.pt`), 결과(`runs/`, `*.csv`, `*.jpg`), 가상환경(`venv/`), 데이터셋(`ball_dataset/`)은 `.gitignore`로 제외했습니다.
모델(`best.pt`)과 학습 코드는 구글 드라이브로 따로 공유합니다.

진행 상황과 확인된 사실은 `CLAUDE.md`에 정리되어 있습니다.
