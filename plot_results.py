import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(r"C:\futsal\runs\detect\ball_v1_s\results.csv", encoding="utf-8")))
def col(sub):
    k = next((k for k in rows[0] if sub in k), None)
    return [float(r[k]) for r in rows] if k else None

ep = col("epoch")
panels = [("train/box_loss", "box loss (train)"), ("train/cls_loss", "cls loss (train)"),
          ("metrics/precision", "precision"), ("metrics/recall", "recall"),
          ("metrics/mAP50(B)", "mAP50"), ("metrics/mAP50-95(B)", "mAP50-95")]
fig, axs = plt.subplots(2, 3, figsize=(13, 7))
for ax, (key, title) in zip(axs.flat, panels):
    y = col(key)
    if y: ax.plot(ep, y)
    ax.set_title(title); ax.set_xlabel("epoch"); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r"C:\futsal\runs\detect\ball_v1_s\my_results.png", dpi=120)
print("saved my_results.png")
