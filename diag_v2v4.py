import csv
from collections import Counter

def load(p):
    return {float(r["t"]): r["status"] for r in csv.DictReader(open(p))}

v2 = load(r"C:\futsal\clip_track_v2.csv")
v4 = load(r"C:\futsal\clip_track_v4.csv")
ts = sorted(v2)

for name, v in (("v2", v2), ("v4", v4)):
    c = Counter(v.values())
    print(f"{name}: detected={c['detected']}  predicted={c['predicted']}  missing={c['missing']}")

def runs(sel):
    out, cur = [], []
    for t in sel:
        if cur and t - cur[-1] > 0.1:
            out.append(cur); cur = []
        cur.append(t)
    if cur:
        out.append(cur)
    return sorted(out, key=lambda g: -len(g))

lost = [t for t in ts if v2[t] == "detected" and v4[t] != "detected"]
gained = [t for t in ts if v4[t] == "detected" and v2[t] != "detected"]
print(f"\nv2에서는 검출이었는데 v4에서는 아닌 프레임 {len(lost)}개 / 반대로 v4에서 새로 검출 {len(gained)}개")
for title, sel in (("v4에서 잃은 구간", lost), ("v4에서 얻은 구간", gained)):
    print(f"\n[{title}] 긴 순서 상위 6개 (클립 초 / 프레임 / 그때 상태)")
    for g in runs(sel)[:6]:
        a, b = g[0], g[-1]
        print(f"  {a-2700:6.2f}~{b-2700:6.2f}초  {len(g):3d}프레임  v2={v2[a]:9s} v4={v4[a]}")
print(f"\n52.08초: v2={v2[min(ts, key=lambda t: abs(t-2752.08))]}  v4={v4[min(ts, key=lambda t: abs(t-2752.08))]}")

