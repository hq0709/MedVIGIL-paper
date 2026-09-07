"""Emit the LaTeX rows of the volumetric table with the 2D columns from MedVIGIL-3D/figdata/headline_3d.csv."""
import csv
rows = list(csv.DictReader(open("/rodata/azradonc_dev/m253405/MedVIGIL-3D/figdata/headline_3d.csv")))
def f(v, signed=False):
    if v in ("", None): return "---"
    x = float(v); return (f"${x:+.1f}$" if signed else f"{x:.1f}")
out = []
for r in rows:
    out.append(f"{r['model']} & {f(r['original'])} & {f(r['pr'])} & {f(r['neg'])} & {f(r['sdr'])} & {f(r['lpa'])} & {f(r['sfr'])} & {f(r['vgr'], True)} & {f(r['cs'])} \\\\")
open("figs/tab_headline3d.tex", "w").write("\n".join(out) + "\n\\bottomrule%\n"); print("\n".join(out))
