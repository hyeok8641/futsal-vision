import csv
trk = list(csv.DictReader(open(r"C:\futsal\clip_track_v2.csv")))
crt = list(csv.DictReader(open(r"C:\futsal\clip_court_v2.csv")))
print("클립초  상태       트랙  신뢰도  화면(u,v)       코트 x,y(m)")
for i, (a, b) in enumerate(zip(trk, crt)):
    t = float(a["t"]) - 2700
    if 51.2 <= t <= 53.1 and i % 2 == 0:
        conf = a["conf"] if a["conf"] else "  -  "
        uv = f"({b['u']:>6},{b['v']:>6})" if b["u"] else "      -       "
        xy = f"{b['x_m']:>6},{b['y_m']:>6}" if b["x_m"] else "     -"
        print(f"{t:6.2f}  {a['status']:9s}  {a['track_id']:>3}  {conf:>6}  {uv}  {xy}")
