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

The analysis scripts read aggregate CSVs under `results/`. They support table and figure analysis; historical probe responses are not bundled:

```bash
# Headline MCS values (Table 1)
python3 analysis/recompute_mcs.py

# Historical bootstrap analysis (requires the original per-probe cache)
python3 analysis/bootstrap_mcs.py

# MCS sensitivity analysis
python3 analysis/mcs_sensitivity.py

# R4 aggregate reproduction from mapped, verified counts
python3 analysis/clinician_baseline_mcs.py

# Original reading-pack validation and complete per-probe scoring:
# follow analysis/README_r4.txt; requires answer sheet, seq_key.csv and gold.csv.
# The private reading pack is not bundled with this source.

# Audit-summary figure (Fig. 3)
python3 analysis/silent_failure/figure_audit_summary.py

# Visual decay figures (Figs. 4 and 6)
python3 analysis/visual_decay/figure_visual_decay.py
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

The paper LaTeX source and analysis scripts in this repository are released under the MIT License (see `LICENSE`). MedVIGIL annotations are released under CC BY-NC-SA 4.0; source assets keep their upstream licences (VQA-RAD CC0, SLAKE CC BY-SA 4.0, ROCO CC BY-NC-SA 4.0). MIMIC-CXR and CheXpert content is withheld under the applicable credentialed data use agreements; see the manuscript's documentation appendix and the dataset datasheet.

## README-scoped revision

The latest revision follows the supplied camera-ready checklist and necessary consistency updates. Broader scientific/editorial rewrites from the preceding revision have been withdrawn pending author confirmation. The abstract retains its original research definition and narrative, with only the checklist-required first-use definition of gold, drafting disclosure and release information synchronized. The original model artwork and unrelated figure generators have been restored.

Funding is disclosed only as grant number 1R01EB038426-01. The authors confirm no competing interests. R4 is Radiology, 20 years; its mapped full-benchmark results remain MCS 83.3, SFR 5.8% and VGR +4.7 pp. The private reading pack, complete image key, nonpublic gold records and credentialed per-probe outputs are not published.

## Latest revision files

- [LaTeX source](neurips_2026.tex)
- [README item scope](revision_notes/readme_scope_2026-10-17.txt) and [revision summary](revision_notes/revision_summary_2026-10-17.txt)
- [Missing experimental results](revision_notes/missing_experiments_2026-10-17.txt)
- [Main-text and appendix change scope](revision_notes/main_appendix_changes_2026-10-17.txt)
- [NeurIPS 2026 requirements audit](revision_notes/neurips_2026_requirements.txt)
- [Corrected Croissant metadata](croissant.json) and [validation notes](revision_notes/croissant_validation.txt)

Compiled manuscript PDFs and marked comparison materials are kept locally. Figure assets needed for compilation remain in the repository. The `paper/` conference copy is synchronized; journal and preprint variants are separate versions.

Missing MedGemma columns and the broader artefact experiment remain open. The corrected metadata here does not imply that the Hugging Face copy or OpenReview forms have been updated. No conference submission or chair message has been performed.
