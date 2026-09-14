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
def axial_crop(arr):
    gut = np.all(arr == 128, axis=(0, 2)); x = int(np.argmax(gut)) if gut.any() else arr.shape[1]
    p = arr[:, :x]; body = p[..., 1] > 30; body[-12:, :] = False
    ys, xs = np.nonzero(body); m = 14
    y0, y1, x0, x1 = max(0, ys.min() - m), min(p.shape[0], ys.max() + m), max(0, xs.min() - m), min(p.shape[1], xs.max() + m)
    side = max(y1 - y0, x1 - x0); cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
    y0, x0 = max(0, cy - side // 2), max(0, cx - side // 2)
    return p[y0:y0 + side, x0:x0 + side]
TITLES = [("plain", "centre slices\nno annotation"), ("bestslice", "slices on which both\nstructures are visible"),
          ("overlay", "centre slices\nlegend names a red outline"), ("identified", "joint-visibility slices\noutlines and a 10 mm bar")]
fig = plt.figure(figsize=(7.2, 3.7)); gs = GridSpec(2, 4, figure=fig, height_ratios=[1.0, 0.86], hspace=0.42, wspace=0.06)
for k, (cond, desc) in enumerate(TITLES):
    ax = fig.add_subplot(gs[0, k]); ax.imshow(thicken(axial_crop(panels[cond]), 1), interpolation="none")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values(): sp.set_edgecolor("#c9c6c1"); sp.set_linewidth(0.6)
    ax.set_title(f"({'abcd'[k]})  \\texttt{{{cond}}}" if False else f"({'abcd'[k]})  {cond}", fontsize=7.2, loc="left", pad=3)
    ax.text(0.5, -0.05, desc, transform=ax.transAxes, ha="center", va="top", fontsize=6.0, color=H.CHARCOAL, linespacing=1.15)
ax = fig.add_subplot(gs[1, :]); ax.imshow(thicken(panels["identified"], 2), interpolation="none"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
for sp in ax.spines.values(): sp.set_edgecolor("#c9c6c1"); sp.set_linewidth(0.6)
ax.set_title("(e)  identified, as the model receives it: axial, coronal and sagittal panels", fontsize=7.2, loc="left", pad=3)
fig.savefig("figs/fig_render.pdf", bbox_inches="tight", dpi=450); plt.close(fig); print("wrote figs/fig_render.pdf")
