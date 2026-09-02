"""Build Figs. 4-7 of the journal version from the raw result files.
Run from journal/:  python figs/build_figs.py
"""
import csv, json, sys, os, numpy as np, collections
sys.path.insert(0, os.path.dirname(__file__)); import house as H
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
D3 = "/rodata/azradonc_dev/m253405/MedVIGIL-3D"
R2D = os.path.join(os.path.dirname(__file__), "..", "..", "results", "blur_aggregate.csv")
LEG = dict(fontsize=6.3, handlelength=1.4, borderpad=0.35, labelspacing=0.3, handletextpad=0.4, columnspacing=1.0)
INK = "#3a3a3a"; MUTED = "#6a6a6a"

# ================= Fig. 4: (a) scatter, marker area = decision gap  (b) per-model dumbbell =================
rows = list(csv.DictReader(open(f"{D3}/figdata/fig10_margin.csv")))
for r in rows:
    r["p"] = float(r["perturbation"]); r["g"] = float(r["gap"]); r["f"] = float(r["flip_rate"])
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
H.panel_title(a, "a", "Perturbation against answer change  (marker area $\\propto$ decision gap)")
# label anchors: name -> (x, y, ha); log x-axis, so every point separates and can be named
lab = {"LLaVA-OneVision-7B": (0.12, 7.5, "left"), "SmolVLM2-2.2B": (0.28, 14.0, "left"), "Qwen2.5-VL-7B": (0.33, -9.0, "right"),
       "Idefics3-8B": (0.71, -9.0, "left"), "Med3DVLM-7B": (0.89, 7.5, "left"),
       "InternVL3-8B": (1.0, 30.3, "left"), "Qwen2.5-VL-32B": (1.5, 48.9, "left"), "Pixtral-12B": (1.12, 59.5, "left"),
       "Qwen3-VL-8B": (2.55, 77.4, "left"), "InternVL3-14B": (2.6, 92.0, "left"),
       "M3D-LaMed-Phi3-4B": (9.6, 27.0, "right"), "M3D-LaMed-Llama2-7B": (4.63, 12.5, "center")}
for r in sorted(rows, key=lambda r: -r["g"]):           # large markers first, small ones on top
    nat = r["input"] == "native"; col = H.FAMILY[H.family(r["model"])]; sz = 14 + 5 * r["g"]
    if nat: a.scatter(r["p"], r["f"], s=sz, marker="s", facecolor="white", edgecolor=col, linewidth=1.2, zorder=3)
    else:   a.scatter(r["p"], r["f"], s=sz, marker="o", color=col, edgecolor="white", linewidth=0.9, alpha=0.92, zorder=4)
    if r["model"] in lab:
        lx, ly, ha = lab[r["model"]]; name = r["model"].replace("-OneVision-7B", "-OV")
        if r["model"] == "Qwen2.5-VL-7B": name = "Qwen2.5-VL-3B / 7B"
        if r["model"] == "Qwen2.5-VL-3B": continue
        a.annotate(name, (r["p"], r["f"]), xytext=(lx, ly), textcoords="data", fontsize=6.6, color=INK, ha=ha, va="center", zorder=5,
                   arrowprops=dict(arrowstyle="-", color="#c4c4c4", lw=0.55, shrinkA=0, shrinkB=3))
a.axhspan(-4, 4, color=H.BAND, zorder=0)
a.annotate("answer never changes", (9.6, -0.3), ha="right", va="center", fontsize=6.8, color=H.GREEN, zorder=5)
a.set_xscale("log"); a.set_xlim(0.08, 10); a.set_xticks([0.1, 0.3, 1, 3, 10]); a.set_xticklabels(["0.1", "0.3", "1", "3", "10"]); a.minorticks_off()
a.set_xlabel("Mean |sighted $-$ blind| log-probability perturbation (nats, log scale)", fontsize=8); a.set_ylabel("Probes whose answer changes (%)", fontsize=8)
a.set_ylim(-14, 100); a.set_yticks([0, 25, 50, 75, 100])
fam = [("Qwen", "Qwen"), ("InternVL", "InternVL"), ("Pixtral", "Pixtral"), ("HF", "HuggingFace"), ("LLaVA", "LLaVA")]
h = [Line2D([], [], marker="o", ms=5, color=H.FAMILY[k], mec="white", ls="none", label=n) for k, n in fam] + \
    [Line2D([], [], marker="s", ms=5, mfc="white", mec=H.FAMILY["native"], mew=1.2, ls="none", label="native (volume input)")]
H.boxed_legend(a, h, loc="upper left", ncol=1, **LEG)
# (b) dumbbell, sorted by answer change; percentages in a column outside the frame
order = sorted(rows, key=lambda r: r["f"])
H.panel_title(b, "b", "Perturbation vs decision gap, per model")
for i, r in enumerate(order):
    col = H.FAMILY[H.family(r["model"])]
    b.plot([r["p"], r["g"]], [i, i], color=col, lw=1.3, alpha=0.55, zorder=2)
    b.plot(r["p"], i, marker="o", ms=5, color=col, mec="white", mew=0.8, ls="none", zorder=3)
    b.plot(r["g"], i, marker="o", ms=5, mfc="white", mec=col, mew=1.2, ls="none", zorder=3)
    b.annotate(f"{r['f']:.0f}%", (1.03, i), xycoords=("axes fraction", "data"), ha="left", va="center", fontsize=6.4, color=INK,
               fontweight="bold" if r["f"] >= 30 else "normal", annotation_clip=False)
b.annotate("answer\nchanges", (1.03, len(order) + 0.55), xycoords=("axes fraction", "data"), ha="left", va="top", fontsize=6.0, color=MUTED, annotation_clip=False)
b.set_yticks(range(len(order))); b.set_yticklabels([r["model"].replace("-OneVision", "-OV").replace("M3D-LaMed-", "M3D-") for r in order], fontsize=6.4)
b.set_xscale("log"); b.set_xlim(0.09, 20); b.set_xticks([0.1, 0.3, 1, 3, 10]); b.set_xticklabels(["0.1", "0.3", "1", "3", "10"]); b.minorticks_off(); b.set_xlabel("nats (log scale)", fontsize=8); b.set_ylim(-0.7, len(order) + 0.6)
hb = [Line2D([], [], marker="o", ms=5, color="#777", mec="white", ls="none", label="perturbation"),
      Line2D([], [], marker="o", ms=5, mfc="white", mec="#777", mew=1.2, ls="none", label="decision gap")]
H.boxed_legend(b, hb, loc="upper left", **LEG)
fig.tight_layout(w_pad=1.6); fig.savefig("figs/fig_flip_rate.pdf", bbox_inches="tight"); plt.close(fig)

# ================= Fig. 5: row 1 accuracy, row 2 modal share =================
rows = list(csv.DictReader(open(f"{D3}/figdata/fig9_roi_four_arm.csv"))); organs = ["Lung", "Colon", "Pancreas", "Liver"]
arms = [("full", "full volume", H.HAZE, "o"), ("roi_masked", "evidence region removed", H.ROSE, "s"), ("roi_only", "only evidence region kept", H.OAT, "^")]
def get(model, o, arm, k): return float(next(r[k] for r in rows if r["model"] == model and r["organ"] == o and r["arm"] == arm))
fig, axes = plt.subplots(2, 2, figsize=(7.0, 3.9), sharex=True, gridspec_kw={"height_ratios": [1.15, 1]})
for j, (letter, model) in enumerate([("a", "Qwen2.5-VL-32B"), ("b", "InternVL3-8B")]):
    ax = axes[0, j]; H.panel_title(ax, letter, f"{model}: accuracy")
    for k, (arm, label, col, mk) in enumerate(arms):
        xs = [i + (k - 1) * 0.24 for i in range(len(organs))]; ys = [get(model, o, arm, "acc") for o in organs]
        lo = [ys[i] - get(model, o, arm, "ci_lo") for i, o in enumerate(organs)]; hi = [get(model, o, arm, "ci_hi") - ys[i] for i, o in enumerate(organs)]
        ax.errorbar(xs, ys, yerr=[lo, hi], fmt=mk, ms=5.5, mfc=col, mec="white", mew=0.9, ecolor=col, elinewidth=1.2, capsize=2, capthick=0.9, zorder=3)
    ax.axhline(50, color=H.GREY, ls="--", lw=1.0, zorder=2); ax.set_ylim(46, 66); ax.set_yticks([50, 55, 60, 65]); ax.set_xlim(-0.6, 3.6)
    ax2 = axes[1, j]; H.panel_title(ax2, chr(ord(letter) + 2), f"{model}: modal answer share")
    for k, (arm, label, col, mk) in enumerate(arms):
        xs = [i + (k - 1) * 0.24 for i in range(len(organs))]; ys = [get(model, o, arm, "modal_share") for o in organs]
        ax2.bar(xs, ys, width=0.22, color=col, edgecolor="none", zorder=3)
        for x, y in zip(xs, ys):
            if arm == "roi_only": H.value_label(ax2, x, y, f"{y:.0f}", col, dy=1.5, size=6.2)
    ax2.axhline(100, color=H.GREY, ls=":", lw=0.8); ax2.set_ylim(40, 104); ax2.set_yticks([50, 75, 100]); ax2.set_xticks(range(len(organs))); ax2.set_xticklabels(organs); ax2.grid(False, axis="x")
axes[0, 0].set_ylabel("Accuracy (%)"); axes[1, 0].set_ylabel("Modal share (%)")
axes[0, 0].annotate("blank volume = 50.0", (1.5, 49.5), ha="center", va="top", fontsize=6.6, color=MUTED)
H.boxed_legend(axes[0, 0], [H.series_handle(c, m, l, ls="none") for _, l, c, m in arms], loc="upper right", ncol=1, **LEG)
fig.tight_layout(h_pad=0.8, w_pad=1.0); fig.savefig("figs/fig_four_arm.pdf", bbox_inches="tight"); plt.close(fig)

# ================= Fig. 6: (a) sub-task bars  (b) distance-answer distribution =================
models = ["Qwen2.5-VL-7B", "InternVL3-8B", "Qwen3-VL-8B", "Qwen2.5-VL-32B"]; tags = ["qwen7b", "internvl", "qwen3vl", "qwen32b"]
xlab = ["Qwen2.5-VL\n7B", "InternVL3\n8B", "Qwen3-VL\n8B", "Qwen2.5-VL\n32B"]
tasks = [("localise, annotated", H.HAZE), ("localise, unannotated", H.LILAC), ("name target", H.SAGE), ("distance (mm)", H.ROSE)]
acc = {"Qwen2.5-VL-7B": [67.7, 57.3, 34.3, 25.7], "InternVL3-8B": [41.0, 15.0, 31.3, 26.3], "Qwen3-VL-8B": [81.7, 49.7, 60.0, 23.0], "Qwen2.5-VL-32B": [76.0, 52.0, 45.0, 28.3]}
ci = {"Qwen2.5-VL-7B": [(61.1, 74.1), (50.0, 64.3), (29.4, 39.5), (20.7, 31.0)], "InternVL3-8B": [(34.1, 48.2), (10.8, 19.6), (26.3, 36.5), (21.6, 31.3)],
      "Qwen3-VL-8B": [(76.4, 86.6), (42.5, 56.8), (54.3, 65.6), (18.3, 27.9)], "Qwen2.5-VL-32B": [(70.4, 81.4), (44.6, 59.2), (39.3, 51.1), (23.1, 33.8)]}
BUCK = ["5", "15", "25", "35"]; dist = {}
for m, t in zip(models, tags):
    R = [json.loads(l) for l in open(f"{D3}/results_new/id_common_{t}_subtask-distance.jsonl")]
    c = collections.Counter(r["prediction"] for r in R); dist[m] = [c.get(k, 0) for k in BUCK]
    if m == models[0]:
        g = collections.Counter(r["gold"] for r in R); dist["gold"] = [g.get(k, 0) for k in BUCK]
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.25, 1]})
H.panel_title(a, "a", "Four sub-tasks on the identified rendering  (chance 25%)"); a.grid(False, axis="x")
X = np.arange(len(models)); w = 0.19; gap = 0.015; hs = []
for j, (name, col) in enumerate(tasks):
    xs = X + (j - 1.5) * (w + gap); ys = [acc[m][j] for m in models]
    lo = [acc[m][j] - ci[m][j][0] for m in models]; hi = [ci[m][j][1] - acc[m][j] for m in models]
    hs.append(a.bar(xs, ys, width=w, color=col, edgecolor="none", label=name, zorder=3))
    a.errorbar(xs, ys, yerr=[lo, hi], fmt="none", ecolor="#555", elinewidth=0.7, capsize=1.5, zorder=4)
hs.append(a.axhline(25, color="#9a9a9a", lw=0.8, ls="-", zorder=2, label="chance 25%"))
for i, m in enumerate(models): H.value_label(a, X[i] + (3 - 1.5) * (w + gap), ci[m][3][1], f"{acc[m][3]:.1f}", H.ROSE, dy=2, size=7)
a.set_xticks(X); a.set_xticklabels(xlab, fontsize=7); a.set_xlim(-0.6, 3.6); a.set_ylim(0, 100); a.set_yticks([0, 25, 50, 75, 100]); a.set_ylabel("Accuracy (%)")
H.boxed_legend(a, hs, loc="upper center", ncol=1, bbox_to_anchor=(0.36, 0.99), fontsize=6.0, handlelength=1.2, borderpad=0.35, labelspacing=0.3, handletextpad=0.4)
H.panel_title(b, "b", "Distance answers: where the 300 items land"); b.grid(False, axis="y")
rowsb = [("gold", dist["gold"])] + [(m, dist[m]) for m in models]
shades = [H.HAZE, H.SAGE, H.OAT, H.ROSE]
for i, (name, d) in enumerate(rowsb):
    left = 0; tot = sum(d)
    for k, (v, colk) in enumerate(zip(d, shades)):
        b.barh(i, v, left=left, color=colk, edgecolor="white", linewidth=0.6, height=0.62, alpha=1.0 if name != "gold" else 0.55, zorder=3)
        if v / tot >= 0.12: b.annotate(f"{v}", (left + v / 2, i), ha="center", va="center", fontsize=6.4, color="white" if name != "gold" else "#333", fontweight="bold")
        left += v
b.set_yticks(range(len(rowsb))); b.set_yticklabels(["gold (n=300)"] + models, fontsize=6.6); b.invert_yaxis()
b.set_xlim(0, 300); b.set_xticks([0, 100, 200, 300]); b.set_xlabel("items", fontsize=8)
hb = [Line2D([], [], marker="s", ms=7, color=c, ls="none", label=f"{k} mm") for k, c in zip(BUCK, shades)]
H.boxed_legend(b, hb, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.42), **LEG)
fig.tight_layout(w_pad=1.4); fig.savefig("figs/fig_subtask.pdf", bbox_inches="tight"); plt.close(fig)

# ================= Fig. 7: decay, 2D and volumetric, plus decision-margin perturbation =================
SIG = [0, 2, 4, 8, 16, 32, 64]; CONDS = [f"sigma{s}" for s in SIG] + ["noimage"]; XP = list(range(len(SIG))) + [len(SIG) + 0.8]
XINF = XP[-1]; CH = "#9a9a9a"
R2 = list(csv.DictReader(open(R2D)))
def acc2d(model, group, s):
    key = "inf" if s == "inf" else str(s)
    return 100 * float(next(r["acc"] for r in R2 if r["model_id"] == model and r["group"] == group and r["tier"] == "all" and r["sigma"] == key))
m2d = [("gpt-4o", "GPT-4o", 64, H.HAZE, "o"), ("claude-sonnet-4-6", "Claude Sonnet 4.6", 32, H.ROSE, "s"),
       ("Qwen--Qwen3.5-397B-A17B", "Qwen3.5-397B", 16, H.LILAC, "^"), ("huatuogpt-vision-7b", "HuatuoGPT-V 7B", 32, H.OAT, "D")]
def load3d(path):
    R = [json.loads(l) for l in open(path)]; by = collections.defaultdict(dict)
    for r in R: by[r["qid"]][r["condition"]] = r
    qs = [q for q, d in by.items() if all(c in d for c in CONDS)]
    acc = {c: 100 * np.mean([by[q][c]["prediction"] == by[q][c]["gold"] for q in qs]) for c in CONDS}
    m = lambda r: r["logprobs"]["yes"] - r["logprobs"]["no"]
    pert = {c: np.array([abs(m(by[q][c]) - m(by[q]["sigma0"])) for q in qs]) for c in CONDS[1:]}
    flips = sum(any(by[q][c]["prediction"] != by[q]["sigma0"]["prediction"] for c in CONDS[1:]) for q in qs)
    return acc, pert, flips, len(qs)
m3d = [(f"{D3}/decay_m3d.jsonl", "M3D-LaMed-Phi3-4B", 8, H.CHARCOAL, "o"), (f"{D3}/decay_qwen7b.jsonl", "Qwen2.5-VL-7B", 0, H.SAGE, "s")]
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.05, 1, 1]})
def chance(ax, y, below=False, left=False):
    ax.axhline(y, color=CH, lw=0.8, zorder=2)
    ax.annotate("chance", (-0.45 if left else XINF + 0.45, y), xytext=(1 if left else -1, -4 if below else 2), textcoords="offset points", ha="left" if left else "right", va="top" if below else "bottom", fontsize=6.3, color=MUTED)
# ---- (a) 2D: four image-required curves, the text-answerable control as one range band
ax = axes[0]; H.panel_title(ax, "a", "2D suite: accuracy"); hs = []
for mid, name, L, col, mk in m2d:
    y = [acc2d(mid, "image_required", s) for s in SIG] + [acc2d(mid, "image_required", "inf")]
    ax.plot(XP[:-1], y[:-1], ls="--", lw=1.0, color=col, marker=mk, ms=4.2, mec="white", mew=0.6, zorder=3)
    ax.plot(XINF, y[-1], marker="x", ms=6, mew=1.5, color=col, mec=col, ls="none", zorder=3)
    hs.append(H.series_handle(col, mk, f"{name} ($L^\\star$={L})"))
hs.append(Line2D([], [], marker="x", ms=6, mew=1.5, color="#666", mec="#666", ls="none", label="no image"))
chance(ax, 20, left=True)
ax.set_ylabel("Accuracy (%)"); ax.set_ylim(0, 100); ax.set_yticks([0, 20, 40, 60, 80, 100])
H.boxed_legend(ax, hs, loc="upper right", fontsize=6.0, handlelength=1.6, borderpad=0.35, labelspacing=0.3)
# ---- (b) volumetric accuracy
ax = axes[1]; H.panel_title(ax, "b", "Volumetric suite: accuracy"); h3 = []; data = {}
for path, name, L, col, mk in m3d:
    acc, pert, flips, n = load3d(path); data[name] = (acc, pert, flips, n, col, mk)
    ax.plot(XP[:-1], [acc[c] for c in CONDS[:-1]], ls="--", lw=1.0, color=col, marker=mk, ms=4.2, mec="white", mew=0.6, zorder=3)
    ax.plot(XINF, acc["noimage"], marker="x", ms=6, mew=1.5, color=col, mec=col, ls="none", zorder=3)
    h3.append(H.series_handle(col, mk, f"{name} ($L^\\star$={L})"))
chance(ax, 50, below=True)
ax.set_ylim(0, 100); ax.set_yticks([0, 20, 40, 60, 80, 100]); ax.tick_params(labelleft=False)
H.boxed_legend(ax, h3, loc="upper right", fontsize=6.4, handlelength=1.6, borderpad=0.35)
# ---- (c) decision-margin shift
ax = axes[2]; H.panel_title(ax, "c", "Volumetric suite: what the image does")
for name, (acc, pert, flips, n, col, mk) in data.items():
    med = [np.median(pert[c]) for c in CONDS[1:]]; lo = [np.percentile(pert[c], 25) for c in CONDS[1:]]; hi = [np.percentile(pert[c], 75) for c in CONDS[1:]]; xs = XP[1:-1]
    ax.fill_between(xs, lo[:-1], hi[:-1], color=col, alpha=0.14, lw=0, zorder=1); ax.plot(xs, med[:-1], ls="--", lw=1.0, color=col, marker=mk, ms=4.2, mec="white", mew=0.6, zorder=3)
    ax.errorbar([XINF], [med[-1]], yerr=[[med[-1] - lo[-1]], [hi[-1] - med[-1]]], fmt="x", ms=6, mew=1.5, color=col, mec=col, ecolor=col, elinewidth=1.0, capsize=3, alpha=0.85, zorder=3)
    if name.startswith("M3D"): H.value_label(ax, xs[-3], med[-4], f"{flips}/{n} answers change", col, dx=0, dy=8, ha="center", va="bottom", size=6.5)
    else: H.value_label(ax, xs[-1], med[-2] + 0.35, f"{flips}/{n} answers change", col, dx=2, dy=0, ha="right", va="bottom", size=6.5)
ax.set_ylabel("|$\\Delta$ decision margin| vs $\\sigma$=0 (nats)"); ax.set_ylim(0, 8); ax.set_yticks([0, 2, 4, 6, 8])
ax.annotate("median, IQR band", (0.9, 7.6), ha="left", va="top", fontsize=6.6, color=MUTED)
for ax in axes:
    ax.set_xticks(XP); ax.set_xticklabels([str(s) for s in SIG] + ["$\\infty$"], fontsize=7); ax.set_xlim(-0.5, XINF + 0.6); ax.set_xlabel("Blur $\\sigma$ (px)")
fig.tight_layout(w_pad=0.9); fig.savefig("figs/fig_decay.pdf", bbox_inches="tight"); plt.close(fig)
print("built figs 4-7")
