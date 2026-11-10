p = r"C:\futsal\track_ball.py"
s = open(p, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, "찾지 못했어요: " + old[:40]
    s = s.replace(old, new)

rep("GATE_MAX = 120", "GATE_MAX = 120\nCH_CONF = 0.7\nCH_BEST_MAX = 0.5")
rep("    out = None\n    if kf is not None:", "    out = None\n    best = None\n    gate = GATE_BASE\n    if kf is not None:")
rep("    if kf is None and out is None:",
"""    if kf is not None and confirmed and (best is None or best[4] <= CH_BEST_MAX):
        far = [c for c in cands if c[4] >= CH_CONF
               and ((c[0] - kf.x[0]) ** 2 + (c[1] - kf.x[1]) ** 2) ** 0.5 > gate]
        if far:
            c = max(far, key=lambda c: c[4])
            seg += 1
            kf = KF(c[0], c[1])
            hits, misses, confirmed = 1, 0, False
            last_wh = (c[2], c[3])
            pending = []
            out = (t, "detected", c[0], c[1], c[2], c[3], c[4], seg)
    if kf is None and out is None:""")
open(r"C:\futsal\track_ball_v5.py", "w", encoding="utf-8").write(s)
print("만들었어요: track_ball_v5.py")
