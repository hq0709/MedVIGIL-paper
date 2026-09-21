"""Single-column 2x2 version of the rendering figure, for the page-limited submission.

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
fig = plt.figure(figsize=(3.45, 2.42)); FW, FH = fig.get_size_inches()
gs = GridSpec(2, 2, figure=fig, top=0.94, bottom=0.07, left=0.02, right=0.98,
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

fig.savefig("figs/fig_render_grid.pdf", dpi=450, bbox_inches="tight", pad_inches=0.01); plt.close(fig)
print("wrote figs/fig_render_grid.pdf")
