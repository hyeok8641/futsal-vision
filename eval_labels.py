import csv, sys, bisect

# 사용법: python eval_labels.py cam1추적csv cam2추적csv 라벨csv 시작오프셋(초)
c1_csv, c2_csv, label_csv = sys.argv[1:4]
offset = float(sys.argv[4])
ERROR_TYPES = ("놓침", "오검출", "예측실패")     # "가림"은 오류가 아니라서 뺌

def load_track(path):
    rows = list(csv.DictReader(open(path)))
    return [(float(r["t"]) - offset, r["status"]) for r in rows]   # (클립 기준 시간, 상태)

labels = list(csv.DictReader(open(label_csv, encoding="utf-8-sig")))

def missing_runs(track):
    runs, start = [], None                        # 박스가 없는(missing) 구간들을 모음
    for k, (t, st) in enumerate(track):
        if st == "missing" and start is None:
            start = t
        if st != "missing" and start is not None:
            runs.append((start, track[k - 1][0]))
            start = None
    if start is not None:
        runs.append((start, track[-1][0]))
    return runs

def error_frames(track, cam):
    bad = {}                                      # 프레임 시간 -> 오류 종류
    for lb in labels:
        if lb["type"] not in ERROR_TYPES or str(cam) not in lb["cam"]:
            continue
        a, b = float(lb["start"]), float(lb["end"])
        for t, _ in track:
            if a - 0.017 <= t <= b + 0.017:       # 한 프레임 간격의 절반만큼 여유
                bad[t] = lb["type"]
    return bad

def report(track, cam):
    n = len(track)
    dt = (track[-1][0] - track[0][0]) / (n - 1)
    cnt = {s: sum(1 for _, st in track if st == s) for s in ("detected", "predicted", "missing")}
    runs = missing_runs(track)
    longest = max(runs, key=lambda r: r[1] - r[0])
    bad = error_frames(track, cam)
    print(f"\n==== cam{cam}  (전체 {n}프레임, {n * dt:.1f}초)")
    print(f"검출 {cnt['detected']}  추정 {cnt['predicted']}  놓침 {cnt['missing']}")
    print(f"끊김 횟수 {len(runs)}번,  최장 끊김 {longest[1] - longest[0] + dt:.2f}초 "
          f"({longest[0]:.2f}~{longest[1]:.2f}s)")
    print(f"1초 이상 끊김: " + ", ".join(f"{a:.1f}~{b:.1f}s" for a, b in runs if b - a + dt >= 1.0))
    for ty in ERROR_TYPES:
        k = sum(1 for v in bad.values() if v == ty)
        print(f"{ty}: {k}프레임 ({k * dt:.2f}초)")
    print(f"오류 없는 프레임 비율: {(n - len(bad)) / n * 100:.1f}%")
    return track

tr1 = report(load_track(c1_csv), 1)
tr2 = report(load_track(c2_csv), 2)

t1 = [t for t, _ in tr1]
pairs = []                                       # (cam1 상태, cam2 상태) 짝
for t, st2 in tr2:
    j = bisect.bisect_left(t1, t)
    k = min((x for x in (j - 1, j) if 0 <= x < len(t1)), key=lambda x: abs(t1[x] - t))
    if abs(t1[k] - t) <= 0.017:                  # 반 프레임 이내면 같은 시각으로 봄
        pairs.append((tr1[k][1], st2))
both_miss = sum(1 for a, b in pairs if a == "missing" and b == "missing")
print(f"\n==== 두 카메라 합쳐서  (시간이 맞는 프레임 {len(pairs)}개)")
print(f"두 카메라 모두 놓친 프레임: {both_miss} ({both_miss / len(pairs) * 100:.1f}%)")
