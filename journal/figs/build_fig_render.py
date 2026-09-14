"""Render one growth-contact probe under the four identification-control conditions,
using the repository's own renderer (no model is run).  Row 1: the axial panel of each
condition, cropped to the body.  Row 2: the full identified montage as the model receives it.
Outlines are thickened for display only.  Run from journal/."""
import sys, os, numpy as np
D3 = "/rodata/azradonc_dev/m253405/MedVIGIL-3D"; MSD = "/rodata/azradonc_dev/m253405/MSD"
sys.path.insert(0, f"{D3}/spatialgen"); sys.path.insert(0, D3)
import run_identification_control as ric
from run_pipeline import label_map
from lesion_binding import LESION_LABEL, find_lesions
from scene_graph import load_ras
sys.path.insert(0, os.path.dirname(__file__)); import house as H
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import binary_dilation
TASK, VID, LK, TARGET = "Task10_Colon", "colon_111", "lesion1", "liver"
vol, affine = load_ras(f"{MSD}/{TASK}/imagesTr/{VID}.nii.gz")
gt, _ = load_ras(f"{MSD}/{TASK}/labelsTr/{VID}.nii.gz")
seg, _ = load_ras(f"{D3}/cfqa_{TASK}/seg_cache/{VID}_seg.nii.gz")
spacing = np.abs(np.diag(affine)[:3]); vol = vol.astype(np.int16)
lesion = dict(find_lesions(gt == LESION_LABEL[TASK], affine))[LK]
name2lab = {v: k for k, v in label_map().items()}; tmask = seg == name2lab[TARGET]
panels = {}
for cond in ric.IMAGE_CONDITIONS:
    arr, geom = ric.render(vol, lesion, tmask, spacing, cond); panels[cond] = arr
    print(cond, arr.shape, {k: v for k, v in geom.items() if not isinstance(v, (list, dict))})
def thicken(arr, it):
    out = arr.copy()
    for rgb in (ric.LESION_RGB, ric.TARGET_RGB, [255, 255, 255]):
        m = np.all(arr == np.array(rgb, dtype=arr.dtype), axis=2)
        if m.any(): out[binary_dilation(m, iterations=it)] = rgb
    return out
from scipy.ndimage import label as cc_label
def body_bbox(p, margin):
    body = p[..., 1] > 30; body[-12:, :] = False
    lab, n = cc_label(body)
    if n > 1:
        sizes = np.bincount(lab.ravel()); sizes[0] = 0; body = lab == sizes.argmax()
    ys, xs = np.nonzero(body)
    return (max(0, ys.min() - margin), min(p.shape[0] - 12, ys.max() + margin), max(0, xs.min() - margin), min(p.shape[1], xs.max() + margin))
def axial_crop(arr):
    gut = np.all(arr == 128, axis=(0, 2)); x = int(np.argmax(gut)) if gut.any() else arr.shape[1]
    p = arr[:, :x]; y0, y1, x0, x1 = body_bbox(p, 10)
    return p[y0:y1, x0:x1]
TITLES = [("plain", "centre slices\nno annotation"), ("bestslice", "slices on which both\nstructures are visible"),
          ("overlay", "centre slices\nlegend names a red outline"), ("identified", "joint-visibility slices\noutlines and a 10 mm bar")]
fig = plt.figure(figsize=(7.2, 4.5)); gs = GridSpec(2, 4, figure=fig, height_ratios=[0.9, 1.35], hspace=0.26, wspace=0.06)
for k, (cond, desc) in enumerate(TITLES):
    ax = fig.add_subplot(gs[0, k]); ax.imshow(thicken(axial_crop(panels[cond]), 1), interpolation="none")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values(): sp.set_edgecolor("#c9c6c1"); sp.set_linewidth(0.6)
    ax.set_title(f"({'abcd'[k]})  \\texttt{{{cond}}}" if False else f"({'abcd'[k]})  {cond}", fontsize=7.2, loc="left", pad=3)
    ax.text(0.5, -0.05, desc, transform=ax.transAxes, ha="center", va="top", fontsize=6.0, color=H.CHARCOAL, linespacing=1.15)
# ---- (e): the three identified panels, each cropped to the body and shown at one physical scale (mm per inch equal across panels)
def split(arr):
    gut = np.all(arr == 128, axis=(0, 2)); cols, start = [], None
    for x, g in enumerate(gut):
        if not g and start is None: start = x
        if g and start is not None: cols.append((start, x)); start = None
    if start is not None: cols.append((start, arr.shape[1]))
    return [arr[:, a:b] for a, b in cols]
def bar_len(p):
    row = p[p.shape[0] - 7, 6:, :]; white = np.all(row == 255, axis=1); n = 0
    while n < len(white) and white[n]: n += 1
    return n
views = []
for p in split(panels["identified"]):
    n = bar_len(p); iso = 10.0 / n if n >= 4 else 0.78
    y0, y1, x0, x1 = body_bbox(p, 6)
    c = thicken(p[y0:y1, x0:x1], 2).copy(); nb = int(round(10.0 / iso)); h = c.shape[0]
    c[h - 10:h - 5, 8:8 + nb] = [255, 255, 255]                      # 10 mm bar re-drawn for the crop
    views.append((c, iso))
# each panel fills the row height, as render.montage scales panels to a common height for the model
ratios = [c.shape[1] / c.shape[0] for c, _ in views]
sub = gs[1, :].subgridspec(1, 3, width_ratios=ratios, wspace=0.03)
for k, ((c, iso), name) in enumerate(zip(views, ["axial", "coronal", "sagittal"])):
    ax = fig.add_subplot(sub[0, k]); ax.imshow(c, interpolation="none"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values(): sp.set_edgecolor("#c9c6c1"); sp.set_linewidth(0.6)
    ax.text(0.03, 0.96, name, transform=ax.transAxes, ha="left", va="top", fontsize=6.4, color="white", bbox=dict(boxstyle="round,pad=0.25", fc="black", ec="none", alpha=0.55))
    if k == 0: ax.set_title("(e)  identified, as the model receives it: the three panels, cropped to the body", fontsize=7.2, loc="left", pad=3)
print("view sizes (px, iso):", [(c.shape, round(iso, 3)) for c, iso in views])
fig.savefig("figs/fig_render.pdf", bbox_inches="tight", dpi=450); plt.close(fig); print("wrote figs/fig_render.pdf")
