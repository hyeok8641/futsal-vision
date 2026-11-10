import csv, sys
p_a, p_b, off = sys.argv[1], sys.argv[2], float(sys.argv[3])
load = lambda p: {float(r["t"]): r["status"] for r in csv.DictReader(open(p))}
a, b = load(p_a), load(p_b)
ts = sorted(a)

def runs(sel):
    out, cur = [], []
    for t in sel:
        if cur and t - cur[-1] > 0.1:
            out.append(cur); cur = []
        cur.append(t)
    if cur:
        out.append(cur)
    return out

lost = [t for t in ts if a[t] == "detected" and b[t] != "detected"]
gained = [t for t in ts if b[t] == "detected" and a[t] != "detected"]
print(f"v2에서는 검출인데 v4에서는 아닌 프레임 {len(lost)}개 / v4에서 새로 검출 {len(gained)}개")
for title, sel in (("v4에서 잃은 구간", lost), ("v4에서 얻은 구간", gained)):
    print(f"\n[{title}] (클립 초)")
    for g in runs(sel):
        print(f"  {g[0]-off:6.2f}~{g[-1]-off:6.2f}초  {len(g)}프레임")
