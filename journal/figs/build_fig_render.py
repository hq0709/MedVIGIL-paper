"""Render one growth-contact probe under the four identification-control conditions,
using the repository's own renderer (no model is run).  Run from journal/."""
import sys, os, numpy as np
D3 = "/rodata/azradonc_dev/m253405/MedVIGIL-3D"; MSD = "/rodata/azradonc_dev/m253405/MSD"
sys.path.insert(0, f"{D3}/spatialgen"); sys.path.insert(0, D3)
import run_identification_control as ric
from run_pipeline import label_map
from lesion_binding import LESION_LABEL, find_lesions
try: load_ras = ric.load_ras
except AttributeError:
    from render import load_ras
sys.path.insert(0, os.path.dirname(__file__)); import house as H
import matplotlib.pyplot as plt
from PIL import Image
TASK, VID, LK, TARGET = "Task03_Liver", "liver_0", "lesion5", "heart"
vol, affine = load_ras(f"{MSD}/{TASK}/imagesTr/{VID}.nii.gz")
gt, _ = load_ras(f"{MSD}/{TASK}/labelsTr/{VID}.nii.gz")
seg, _ = load_ras(f"{D3}/cfqa_{TASK}/seg_cache/{VID}_seg.nii.gz")
spacing = np.abs(np.diag(affine)[:3]); vol = vol.astype(np.int16)
lesions = dict(find_lesions(gt == LESION_LABEL[TASK], affine)); lesion = lesions[LK]
name2lab = {v: k for k, v in label_map().items()}; tmask = seg == name2lab[TARGET]
print("lesion voxels", int(lesion.sum()), "target voxels", int(tmask.sum()), "spacing", spacing)
panels = {}
for cond in ric.IMAGE_CONDITIONS:
    arr, geom = ric.render(vol, lesion, tmask, spacing, cond)
    panels[cond] = arr; Image.fromarray(arr).save(f"figs/render_{cond}.png")
    print(cond, arr.shape, {k: v for k, v in geom.items() if not isinstance(v, (list, dict))})
titles = {"plain": "plain: the published input (centre slices, no annotation)",
          "bestslice": "bestslice: slices chosen so both structures are visible",
          "overlay": "overlay: centre slices, lesion in red, target in cyan",
          "identified": "identified: joint-visibility slices, outlines and a 10 mm bar"}
fig, axes = plt.subplots(2, 2, figsize=(7.2, 2.75))
for ax, (letter, cond) in zip(axes.ravel(), zip("abcd", ric.IMAGE_CONDITIONS)):
    ax.imshow(panels[cond]); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values(): sp.set_edgecolor("#c9c6c1"); sp.set_linewidth(0.6)
    ax.set_title(f"({letter})  {titles[cond]}", fontsize=6.8, loc="left", pad=3)
fig.tight_layout(w_pad=0.6, h_pad=1.4); fig.savefig("figs/fig_render.pdf", bbox_inches="tight", dpi=300); plt.close(fig)
print("wrote figs/fig_render.pdf")
