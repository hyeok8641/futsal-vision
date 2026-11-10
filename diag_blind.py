import csv, bisect
from statistics import median

OFF = 2400.0
load = lambda p: {float(r["t"]): r for r in csv.DictReader(open(p))}
c1 = load(r"C:\futsal\clip40_court_v2.csv")
c2 = load(r"C:\futsal\clip40c2_court.csv")
t2 = sorted(c2)
xy = lambda r: (float(r["x_m"]), float(r["y_m"])) if r["x_m"] != "" else None

def near2(t):
    j = bisect.bisect_left(t2, t)
    c = [k for k in (j - 1, j) if 0 <= k < len(t2)]
    if not c:
        return None
    k = min(c, key=lambda k: abs(t2[k] - t))
    return t2[k] if abs(t2[k] - t) <= 0.02 else None

print("[1] cam1이 못 보던 구간에서 cam2는?")
for a, b in ((34.35, 37.45), (38.38, 41.42)):
    ts = [t for t in t2 if a <= t - OFF <= b]
    st = [c2[t]["status"] for t in ts]
    pts = [xy(c2[t]) for t in ts if c2[t]["status"] == "detected" and xy(c2[t])]
    print(f"  {a}~{b}초: cam2 {len(ts)}프레임 중 검출 {st.count('detected')} / 예측 {st.count('predicted')} / 없음 {st.count('missing')}")
    if pts:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        print(f"     cam2 검출의 코트 좌표 중앙값 x={median(xs):.1f} y={median(ys):.1f} m  (x {min(xs):.1f}~{max(xs):.1f}, y {min(ys):.1f}~{max(ys):.1f})")

print("\n[2] cam1 의심 박스 vs 같은 시각 cam2 (2프레임마다 출력)")
for name, a, b, tag in (("궤적12", 37.48, 37.55, "오검출 확인"), ("궤적13", 38.08, 38.35, "미확인"),
                        ("궤적16", 41.45, 42.12, "오검출 확인"), ("궤적18", 42.72, 42.82, "미확인")):
    print(f"  {name} {a}~{b}초 ({tag})")
    n = 0
    for t in sorted(c1):
        ct = t - OFF
        if not a <= ct <= b or c1[t]["status"] == "missing":
            continue
        n += 1
        if n % 2 == 0:
            continue
        r1, p1 = c1[t], xy(c1[t])
        k = near2(t)
        r2 = c2.get(k) if k is not None else None
        p2 = xy(r2) if r2 and r2["status"] != "missing" else None
        s1 = f"cam1 {r1['status'][:4]} ({p1[0]:.1f},{p1[1]:.1f})" if p1 else "cam1 좌표없음"
        if p2:
            d = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5 if p1 else None
            s2 = f"cam2 {r2['status'][:4]} ({p2[0]:.1f},{p2[1]:.1f})" + (f"  거리 {d:.1f} m" if d is not None else "")
        else:
            s2 = "cam2 없음"
        print(f"    {ct:6.2f}초  {s1}  |  {s2}")
