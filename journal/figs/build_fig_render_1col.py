"""Single-column version of the rendering figure, for the page-limited submission.

Same probe, same slice selection, windowing, orientation and resampling as
build_fig_render.py; only the layout changes: the four conditions sit in a 2x2
grid and the three identified planes run along one physical scale underneath.
Run from journal/.
"""
import sys, os, numpy as np
D3 = "/rodata/azradonc_dev/m253405/MedVIGIL-3D"; MSD = "/rodata/azradonc_dev/m253405/MSD"
sys.path.insert(0, f"{D3}/spatialgen"); sys.path.insert(0, D3)
import run_identification_control as ric
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_fig_render as base                                   # geometry, drawing, the probe itself
import house as H
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

P = base.P
fig = plt.figure(figsize=(3.45, 3.78)); FW, FH = fig.get_size_inches()
gs = GridSpec(2, 2, figure=fig, top=0.962, bottom=0.445, left=0.02, right=0.98,
              wspace=0.04, hspace=0.20)
TITLES = [("plain", "centre slices, no annotation"),
          ("bestslice", "both structures visible"),
          ("overlay", "centre slices, outlines"),
          ("identified", "outlines and a 10 mm bar")]

def pad_to(crop, shape, h_px, w_px):
    """Grow a crop symmetrically to a fixed pixel size, so the four panels share one frame."""
    y0, y1, x0, x1 = crop

    def grow(lo, hi, want, limit):
        extra = want - (hi - lo)
        lo -= extra // 2; hi += extra - extra // 2
        if lo < 0: hi -= lo; lo = 0
        if hi > limit: lo -= hi - limit; hi = limit
        return max(0, lo), min(limit, hi)
    y0, y1 = grow(y0, y1, h_px, shape[0])
    x0, x1 = grow(x0, x1, w_px, shape[1])
    return y0, y1, x0, x1


crops = {cond: base.body_bbox(P[cond][0][0], 4) for cond, _ in TITLES}
H_PX = max(c[1] - c[0] for c in crops.values())
W_PX = max(c[3] - c[2] for c in crops.values())
for k, (cond, desc) in enumerate(TITLES):
    g, le, tg, iso = P[cond][0]                                   # the axial panel
    ax = fig.add_subplot(gs[k // 2, k % 2])
    base.draw(ax, g, le, tg, iso, 0.75, annotate=cond in ("overlay", "identified"),
              bar=cond == "identified", crop=pad_to(crops[cond], g.shape, H_PX, W_PX))
    ax.set_title(f"({'abcd'[k]})  {cond}", fontsize=6.4, loc="left", pad=1.8)
    ax.text(0.5, -0.035, desc, transform=ax.transAxes, ha="center", va="top",
            fontsize=5.4, color=H.CHARCOAL)

# (e) the three identified panels at ONE physical scale, top-aligned
views = [(g, le, tg, iso, base.body_bbox(g, 6)) for g, le, tg, iso in P["identified"]]
w_mm = [(c[3] - c[2]) * iso for g, le, tg, iso, c in views]
h_mm = [(c[1] - c[0]) * iso for g, le, tg, iso, c in views]
GAP = 0.05; LEFT, RIGHT = 0.02 * FW, 0.98 * FW; ROW_TOP, ROW_BOT = 0.365 * FH, 0.02 * FH
scale = min((RIGHT - LEFT - 2 * GAP) / sum(w_mm), (ROW_TOP - ROW_BOT) / max(h_mm))
x = LEFT + ((RIGHT - LEFT) - (sum(w_mm) * scale + 2 * GAP)) / 2
fig.text(0.02, (ROW_TOP + 0.04) / FH,
         "(e)  identified, as the model receives it: one physical scale",
         fontsize=6.6, ha="left", va="bottom")
for k, ((g, le, tg, iso, crop), name) in enumerate(zip(views, ["axial", "coronal", "sagittal"])):
    w_in, h_in = w_mm[k] * scale, h_mm[k] * scale
    ax = fig.add_axes([x / FW, (ROW_TOP - h_in) / FH, w_in / FW, h_in / FH])
    base.draw(ax, g, le, tg, iso, 0.9, annotate=True, bar=True, crop=crop)
    ax.text(0.04, 0.95, name, transform=ax.transAxes, ha="left", va="top", fontsize=5.6,
            color="white", bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="none", alpha=0.55))
    x += w_in + GAP
fig.savefig("figs/fig_render_1col.pdf", dpi=450, bbox_inches="tight", pad_inches=0.01); plt.close(fig)
print("wrote figs/fig_render_1col.pdf")
