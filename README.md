# MedVIGIL — Paper LaTeX Source

This repository contains the LaTeX source, figures, analysis scripts, and reproducibility artifacts for the MedVIGIL paper:

> **MedVIGIL: Evaluating Trustworthy Medical VLMs Under Broken Visual Evidence**

**Project page:** <https://hq0709.github.io/MedVIGIL-page/>
**Public dataset (240 cases, 2,002 MCQ probes with open-ended twins, 180 counterfactual triplets):** <https://huggingface.co/datasets/jhq0709/MedVIGIL>
**Evaluation harness:** <https://github.com/hq0709/MedVIGIL>

The full benchmark has 300 cases, 2,556 probes and 240 triplets. Its 60 credentialed chest-radiograph cases are withheld in their entirety: no images, report text, case records or case-to-source mappings are public. Qualified users must verify their own upstream access before requesting the chest-radiograph arm under the applicable data use agreements; see [CXR_ACCESS.md](https://huggingface.co/datasets/jhq0709/MedVIGIL/blob/5373ecdc8e20c467f1933b314b3a3164d2cba6d5/CXR_ACCESS.md).

The public release includes the five data tables, 240 source images, 540 perturbed images, a pilot-ablation summary, and root-level [DATASHEET.md](https://huggingface.co/datasets/jhq0709/MedVIGIL/blob/5373ecdc8e20c467f1933b314b3a3164d2cba6d5/DATASHEET.md), [PIPELINE.md](https://huggingface.co/datasets/jhq0709/MedVIGIL/blob/5373ecdc8e20c467f1933b314b3a3164d2cba6d5/PIPELINE.md) and [croissant.json](https://huggingface.co/datasets/jhq0709/MedVIGIL/blob/5373ecdc8e20c467f1933b314b3a3164d2cba6d5/croissant.json). GPT-5.5 drafted the text perturbations, false-premise traps and V-CF conditions; R1 and R2 reviewed and edited every draft, and P3 finalised every released field.

Release inventory checked at dataset revision `5373ecdc8e20c467f1933b314b3a3164d2cba6d5` and harness revision `abda0797cce67b5f3205817bcb796945b6fe7277`. Neither release contains the historical per-model response caches or `scripts/expand_probes.py`; the harness consumes the released probe CSVs directly.

## Repository layout

```
./       # Camera-ready LaTeX source
  neurips_2026.tex            # Main manuscript (single-file)
  ref.bib                     # Bibliography
  neurips_2026.sty            # conference style file (vendored)
  checklist.tex               # reproducibility checklist
  figures/                    # All figures (PDF/PNG/SVG)
  icons/                      # Provider/model logo icons
  fonts/                      # Embedded fonts
paper/                       # Synchronized duplicate conference source

analysis/                     # Scripts that produce paper tables and figures
  recompute_mcs.py            # MCS recompute under corrected PR (Table 1)
  bootstrap_mcs.py            # Case-clustered bootstrap CIs (Table 12)
  mcs_sensitivity.py          # Weight & Grounding sensitivity (Table 13)
  prepare_r4_inputs.py       # Validate reading key and gold metadata
  score_r4.py                # Strict R4 per-probe scoring
  clinician_baseline_mcs.py   # Recompute verified reference from exact counts
  silent_failure/             # MCS audit-summary figure generator
  visual_decay/               # Visual decay ablation aggregation + figures

results/                      # Aggregated CSVs the figures/tables read from
  metrics_summary.csv
  metrics_by_kind.csv
  metrics_by_source.csv
  metrics_by_tier.csv
  sfr_by_tier.csv
  bootstrap_ci.csv
  mcs_sensitivity.csv
  metrics_mcs_recomputed.csv

data/
  clinician_baseline.csv      # Verified family/tier counts from mapped R4 answers
```

## Building the PDF locally

```bash
tectonic neurips_2026.tex
```

Output: `neurips_2026.pdf` (generated locally; compiled manuscript PDFs are not tracked). Check the compiled main-text page count before submission.

If you do not have tectonic, `latexmk -pdf neurips_2026.tex` works with TeX Live 2023 or newer; the `.bbl` is regenerated from `ref.bib` on first run.

## Reproducing tables and figures

The analysis scripts read aggregate CSVs under `results/`. Historical model-response caches are not bundled; the public R4 clinician responses are available under `data/r4_public/`:

```bash
# Headline MCS values (Table 1)
python3 analysis/recompute_mcs.py

# Historical bootstrap analysis (requires the original per-probe cache)
python3 analysis/bootstrap_mcs.py

# MCS sensitivity analysis
python3 analysis/mcs_sensitivity.py

# R4 aggregate reproduction from mapped, verified counts
python3 analysis/clinician_baseline_mcs.py

# Public R4 per-probe reproduction (240 cases, 2,002 responses)
python3 analysis/score_r4.py --answers data/r4_public/answers.csv --probes data/r4_public/probes_mcq.csv --manifest data/r4_public/manifest.csv --seq-map data/r4_public/seq_to_probe.csv --require-complete --reference-scope public --output-dir r4_public_recomputed

# Full per-probe scoring additionally requires the author-held private inputs.
# See analysis/README_r4.txt for population definitions and complete commands.

# Audit-summary figure (Fig. 3)
python3 analysis/silent_failure/figure_audit_summary.py

# Revised overall visual decay (Fig. 4); retain the current tier plot (Fig. 6)
python3 analysis/visual_decay/figure_visual_decay.py --skip-per-tier
```

For a fresh evaluation, follow the [harness instructions](https://github.com/hq0709/MedVIGIL/blob/abda0797cce67b5f3205817bcb796945b6fe7277/scripts/README.md). The public subset covers 2,002 probes; evaluation on all 2,556 additionally requires the credentialed arm. The historical per-model response caches are not bundled in this repository.

## Citation

```bibtex
@inproceedings{jiang2026medvigil,
  title  = {MedVIGIL: Evaluating Trustworthy Medical VLMs Under Broken Visual Evidence},
  author = {Jiang, Hanqi and Chen, Junhao and Pan, Yi and Chen, Lifeng and You, Weihang and Gong, Haozhen and Yan, Ruiyu and Lv, Jinglei and Zhao, Lin and Ren, Hui and Li, Quanzheng and Liu, Tianming and Li, Xiang},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS), Evaluations and Datasets Track},
  year   = {2026}
}
```

## License

The paper LaTeX source and analysis scripts in this repository are released under the MIT License (see `LICENSE`). MedVIGIL-authored annotations and benchmark metadata are CC BY 4.0 under the canonical [evaluation-repository LICENSE](https://github.com/hq0709/MedVIGIL/blob/main/LICENSE). Source content retains its upstream terms: VQA-RAD CC0, SLAKE research-use, and ROCO MIT-style metadata over PMC-OA images with their original per-image licences. MedVIGIL does not relicense source imagery or other upstream content. MIMIC-CXR and CheXpert content is withheld under the applicable credentialed data use agreements; see the manuscript's documentation appendix and the dataset datasheet.

## Strict README revision

The latest revision applies only the supplied camera-ready checklist and the authors' confirmed details. Content changes made to expand the main text or broadly trim the appendix have been withdrawn; the latest author affiliations are retained. The abstract keeps its original opening, definition, enumeration, narrative and R4 result sentence, with only the required gold definition, drafting/finalisation disclosure and release scope updated. The author-confirmed visual-decay revision updates Table 16, its discussion and Figure 4 from the revised summary percentages. Figure 6 retains the original 296-case tier records with an explicit subset caption. See [visual-decay reproduction notes](analysis/visual_decay/REVISED_SUMMARY.md) for the distinction between the two summaries.

Funding is disclosed only as grant number 1R01EB038426-01. The authors confirm no competing interests. R4 is Radiology, 20 years; its mapped full-benchmark results remain MCS 83.3, SFR 5.8% and VGR +4.7 pp. The private reading pack, complete image key, nonpublic gold records and credentialed per-probe outputs are not published.

## Latest revision files

- [LaTeX source](neurips_2026.tex)
- [Strict README scope and revision summary](revision_notes/readme_scope_2026-10-18.txt)
- [Missing experimental results](revision_notes/missing_experiments_2026-10-17.txt)
- [NeurIPS 2026 requirements audit](revision_notes/neurips_2026_requirements.txt)
- [Corrected Croissant metadata](croissant.json) and [validation notes](revision_notes/croissant_validation.txt)

Compiled manuscript PDFs and marked comparison materials are kept locally. Figure assets needed for compilation remain in the repository. The `paper/` conference copy is synchronized; journal and preprint variants are separate versions.

Missing MedGemma columns and the broader artefact experiment remain open. The corrected metadata here does not imply that the Hugging Face copy or OpenReview forms have been updated. No conference submission or chair message has been performed.

The public R4 answer release and reproducibility instructions are at https://github.com/JunhaoChenMichael/MedVIGIL/tree/ad805039ef9ae0eb406b23fd321d8a176da47c73/data/r4_public. It contains 2,002 public-subset answers from 240 cases (MCS 82.7), with separate full-benchmark aggregate counts (MCS 83.3). All 60 credentialed CXR cases remain excluded from public per-probe records.

Upstream integration is proposed in https://github.com/hq0709/MedVIGIL/pull/1. The answer package is already public at the immutable release link above; it is not yet merged into the upstream main branch.
