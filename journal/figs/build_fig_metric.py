"""Metric-channel control figure: (a) the three backgrounds for one item, (b) accuracy per model x background.
Run from journal/ after MedVIGIL-3D/analysis/metric_control.py has written figdata/metric_control.csv."""
import csv, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import house as H
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image
D3 = "/rodata/azradonc_dev/m253405/MedVIGIL-3D"
ITEM = ("Task10_Colon", "colon_022_lesion1_duodenum")
rows = list(csv.DictReader(open(f"{D3}/figdata/metric_control.csv")))
for r in rows:
    for k in ("acc", "lo", "hi", "modal_share"): r[k] = float(r[k])
MODELS = ["Qwen2.5-VL-7B", "InternVL3-8B", "Qwen3-VL-8B", "Qwen2.5-VL-32B"]
BG = [("grey", "synthetic outlines, grey", H.SAGE), ("ct", "synthetic outlines on CT", H.OAT), ("real", "real lesion and target", H.ROSE)]
fig = plt.figure(figsize=(7.2, 3.1)); gs = GridSpec(3, 2, figure=fig, width_ratios=[0.62, 1.25], hspace=0.28, wspace=0.05)
# (a) one axial panel per background, cropped around the structures
def axial(path):
    im = np.array(Image.open(path).convert("RGB")); gut = np.all(im == 128, axis=(0, 2)); x = int(np.argmax(gut)) if gut.any() else im.shape[1]
    return im[:, :x]
for i, (bg, lab, col) in enumerate(BG):
    ax = fig.add_subplot(gs[i, 0])
    p = f"{D3}/render_cache/synthetic/{bg}/{ITEM[1]}.png" if bg != "real" else f"{D3}/render_cache/{ITEM[0]}/{ITEM[1]}_slices3.png"
    im = axial(p); h, w = im.shape[:2]
    ann = (np.abs(im[..., 0].astype(int) - im[..., 1].astype(int)) > 40) | (np.abs(im[..., 1].astype(int) - im[..., 2].astype(int)) > 40)   # red / cyan outline pixels
    ann[h - 12:, :] = False                                                                                                                 # not the scale bar
    ys, xs = np.nonzero(ann); m = 45
    y0, y1, x0, x1 = max(0, ys.min() - m), min(h, ys.max() + m), max(0, xs.min() - m), min(w, xs.max() + m)
    side = max(y1 - y0, x1 - x0); cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
    y0, x0 = max(0, cy - side // 2), max(0, cx - side // 2); crop = im[y0:y0 + side, x0:x0 + side]
    from scipy.ndimage import binary_dilation
    ca = ann[y0:y0 + side, x0:x0 + side]; crop = crop.copy()
    for col_, mask in ((np.array([255, 60, 60]), ca & (crop[..., 0] > crop[..., 2])), (np.array([60, 200, 255]), ca & (crop[..., 2] > crop[..., 0]))):
        crop[binary_dilation(mask, iterations=2)] = col_                       # display only: thicken the 1-px outlines
    ax.imshow(crop, interpolation="bilinear"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values(): sp.set_edgecolor(col); sp.set_linewidth(1.2)
    ax.set_ylabel(lab, fontsize=6.6, color=H.CHARCOAL, rotation=0, ha="right", va="center", labelpad=6)
fig.text(0.02, 0.97, "(a)  the same question on three backgrounds", fontsize=8, ha="left", va="top")
# (b) grouped bars
ax = fig.add_subplot(gs[:, 1]); H.panel_title(ax, "b", "Distance sub-task accuracy (chance 25%)"); ax.grid(False, axis="x")
X = np.arange(len(MODELS)); w = 0.26; gap = 0.02; hs = []
for k, (bg, lab, col) in enumerate(BG):
    ys, lo, hi = [], [], []
    for m in MODELS:
        r = next((r for r in rows if r["model"] == m and r["background"] == bg), None)
        ys.append(r["acc"] if r else np.nan); lo.append(r["acc"] - r["lo"] if r else 0); hi.append(r["hi"] - r["acc"] if r else 0)
    xs = X + (k - 1) * (w + gap)
    hs.append(ax.bar(xs, ys, width=w, color=col, edgecolor="none", label=lab, zorder=3)); ax.errorbar(xs, ys, yerr=[lo, hi], fmt="none", ecolor="#555", elinewidth=0.7, capsize=1.5, zorder=4)
ax.axhline(25, color="#9a9a9a", lw=0.8, zorder=2)
ax.set_xticks(X); ax.set_xticklabels([m.replace("Qwen2.5-VL-", "Qwen2.5-VL\n").replace("InternVL3-8B", "InternVL3\n8B").replace("Qwen3-VL-8B", "Qwen3-VL\n8B") for m in MODELS], fontsize=7)
ax.set_xlim(-0.6, len(MODELS) - 0.4); ax.set_ylim(0, 100); ax.set_yticks([0, 25, 50, 75, 100]); ax.set_ylabel("Accuracy (%)")
H.boxed_legend(ax, hs, loc="upper right", fontsize=6.2, handlelength=1.2, borderpad=0.4, labelspacing=0.3)
fig.savefig("figs/fig_metric.pdf", bbox_inches="tight"); plt.close(fig); print("wrote figs/fig_metric.pdf")
