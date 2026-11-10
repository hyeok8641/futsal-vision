import csv
import numpy as np

raw = list(csv.DictReader(open(r"C:\futsal\clip_raw.csv")))
trk = list(csv.DictReader(open(r"C:\futsal\clip_track.csv")))

def tracked_conf(t0, t1):
    return [float(r["conf"]) for r in trk
            if r["status"] == "detected" and r["conf"] != "" and t0 <= float(r["t"]) <= t1]

def cands_conf(t0, t1):
    return [float(r["conf"]) for r in raw if r["conf"] != "" and t0 <= float(r["t"]) <= t1]

def show(name, v):
    if not v:
        print(f"{name}: 없음"); return
    a = np.array(v)
    print(f"{name}: 개수={len(a)}  최소={a.min():.2f}  중앙값={np.median(a):.2f}  최대={a.max():.2f}")

print("[전체 클립] 궤적에 쓰인 검출")
show("  전체", tracked_conf(2700, 2761))
print("[구간 A: 0:52~0:54, 먼 모서리 신발]")
show("  궤적에 쓰인 검출", tracked_conf(2752, 2754))
show("  이 구간 모든 후보", cands_conf(2752, 2754))
print("[구간 B: 0:32~0:33, 가림 + 신발 왕복]")
show("  궤적에 쓰인 검출", tracked_conf(2732, 2733.5))
show("  이 구간 모든 후보", cands_conf(2732, 2733.5))
print("[기준: 신발이 아닌 구간 0:05~0:20]")
show("  궤적에 쓰인 검출", tracked_conf(2705, 2720))
