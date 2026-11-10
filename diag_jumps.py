import csv
import numpy as np

rows = list(csv.DictReader(open(r"C:\futsal\clip_court.csv")))
pts = [r for r in rows if r["x_m"] != ""]
xy = lambda r: (float(r["x_m"]), float(r["y_m"]))

out_x_hi = sum(xy(r)[0] > 21 for r in pts)
out_x_lo = sum(xy(r)[0] < -21 for r in pts)
out_y = sum(abs(xy(r)[1]) > 11 for r in pts)
out_det = sum(r["status"] == "detected" and (abs(xy(r)[0]) > 21 or abs(xy(r)[1]) > 11) for r in pts)
out_pred = sum(r["status"] == "predicted" and (abs(xy(r)[0]) > 21 or abs(xy(r)[1]) > 11) for r in pts)
print(f"코트 밖: x>21={out_x_hi}, x<-21={out_x_lo}, |y|>11={out_y}  (검출 {out_det}, 예측 {out_pred})")

jumps = []
for a, b in zip(pts[:-1], pts[1:]):
    if a["track_id"] != b["track_id"]:
        continue
    dt = float(b["t"]) - float(a["t"])
    if not 0 < dt < 0.2:
        continue
    (xa, ya), (xb, yb) = xy(a), xy(b)
    v = np.hypot(xb - xa, yb - ya) / dt
    if v > 30:
        du = np.hypot(float(b["u"]) - float(a["u"]), float(b["v"]) - float(a["v"]))
        jumps.append((v, a, b, du, dt, xa, ya, xb, yb))
jumps.sort(key=lambda j: -j[0])
print(f"\n튀는 지점 {len(jumps)}개 (속도 상위 15개)")
for v, a, b, du, dt, xa, ya, xb, yb in jumps[:15]:
    print(f"t={float(b['t']):.2f}  {a['status']}→{b['status']}  dt={dt:.2f}s  화면이동={du:.0f}px  "
          f"({xa:.1f},{ya:.1f})→({xb:.1f},{yb:.1f}) m  속도={v:.0f} m/s")
far = sum(1 for j in jumps if max(j[5], j[7]) > 12)
pred_before = sum(1 for j in jumps if j[1]["status"] == "predicted")
print(f"\n튀는 지점 중 x>12m(cam1에서 먼 쪽) {far}개, 직전이 예측 상태 {pred_before}개")
