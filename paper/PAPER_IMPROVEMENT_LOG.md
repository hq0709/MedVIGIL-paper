# MedVIGIL — NeurIPS 2026 D&B Track Paper Improvement Log

Reviewer model: GPT-5.4 (xhigh reasoning effort) via Codex MCP, fresh thread per round (REVIEWER_BIAS_GUARD = true).

## Score Progression

| Round | Score | Verdict | Key Changes |
|-------|-------|---------|-------------|
| Round 0 (original) | 5/10 | Almost | Baseline: 23 pages incl. appendix |
| Round 1 | 6/10 | Almost | Fixed PR=accuracy, scoped TR-coh, replaced broken pipeline figure, added Reproducibility / Bootstrap / PCons / Documentation appendices |
| Round 2 (final) | (deferred, see "open items" — see Optional Round 3) | Almost | Regenerated audit summary figures with corrected Cap, added MCS sensitivity, scoped MCQ-only audit, added missing source citations |

**Net improvement: +1 point. Final draft is "Almost ready" — the remaining open items are content-creation tasks (clinician baseline, persistent identifier resolution) rather than writing/format issues.**

## Round 0 Snapshot

The original draft already had: well-scoped contribution, paired-probe design, clinician-supervised pipeline, 16-model audit, blur-decay ablation. Reviewer flagged five blocking issues:

1. **CRITICAL — PR not correctness-conditioned.** PR was anchor/T-CF agreement, so a consistently-wrong model could still appear "robust." PR was used in Cap → MCS, contaminating the headline metric.
2. **CRITICAL — TR-coh advertised but never reported.** The headline metric list claimed eight metrics including triplet coherence, but no model had a per-model TR-coh value because the V-CF probe arm was never scored.
3. **CRITICAL — Figure 2 (pipeline) showed literal placeholder text** in the compiled PDF.
4. **MAJOR — D&B documentation aspirational not concrete.** No IAA numbers, no license matrix, no Croissant pointer, no datasheet, no DOI.
5. **MAJOR — Reproducibility underspecified.** No prompt template, no decoding settings, no model snapshots, no parser/retry rules.
6. **MAJOR — No uncertainty analysis.** With 300 cases and close MCS values, the ranking needed bootstrap CIs.
7. **MAJOR — Internal inconsistency on blur.** §6.4 includes a blur ablation but limitations said "blur is not part of the audit."
8. **MAJOR — `f` notation reused** for build-time triplet invariants and model outputs.
9. **MINOR — LPL ("leakage") name suggested negative connotation** even though high values are good.

## Round 1 Review & Fixes

<details>
<summary>GPT-5.4 xhigh review (Round 1) — full text</summary>

**Overall Score**: 5/10

**Summary**

This is a promising Datasets & Benchmarks paper on an important and under-evaluated failure mode: whether medical VLMs fail safely when the visual evidence contract is broken. The paired-probe design, clinician involvement, and broad 16-model audit are real strengths, but the current draft is not yet submission-ready because the metric formulation is not fully rigorous, a core triplet metric is never actually reported, and the dataset/reproducibility documentation is still too incomplete for NeurIPS D&B.

**Strengths**

- Identifies a meaningful gap beyond standard medical VQA accuracy: evidence-conditional safe failure under false premises and broken visual evidence.
- Paired design is well chosen — clean controls, hallucination traps, ROI-only/ROI-masked variants, laterality flips, and no-image/blur ablations make the failure analysis much more diagnostic than a plain leaderboard.
- Clinician-supervised construction pipeline is a strong asset: CRT risk tiers, text-only-answerability flags, ROI boxes, adjudicated refusal options.
- Empirical audit is substantial: 16 vision-capable systems, matched no-image controls, useful visual-decay ablation.

**Weaknesses**

- `CRITICAL`: The metric story is not fully rigorous. `PR` is defined as anchor/T-CF agreement, not correctness, yet it enters `Cap` on equal footing with accuracy terms in Eq. 3; a model can be "robust" while being consistently wrong. The notation around triplet invariants also reuses `f` as if it were a build-time dataset invariant, even though `f` is defined as the model in Sec. 3.1.
- `CRITICAL`: A core claimed metric is missing from the results. `TR-coh` is advertised as a headline metric but does not appear in Table 1 or any appendix result table.
- `MAJOR`: D&B documentation is still aspirational rather than concrete. The paper says inter-annotator agreement is logged and benchmark metadata/cards/versioning exist, but provides no actual agreement numbers, no license table, no hosting URL/DOI/PID, and no concrete Croissant artifact.
- `MAJOR`: Reproducibility of the evaluation harness is underspecified.
- `MAJOR`: There is no uncertainty analysis.
- `MAJOR`: The paper is internally inconsistent about blur. Section 6.4 includes a full-image Gaussian blur audit, but the limitations say blur is not part of the current empirical audit.
- `MAJOR`: Figure 2 looks unfinished — the extracted PDF text shows literal `fig_pipeline.pdf placeholder`.
- `MINOR`: `LPL` is a confusing name because the table treats higher values as better, even though "leakage" sounds undesirable.
- `MINOR`: Table 1 is well organized but very dense.
- `MINOR`: The appendix surfaces broader MedVIGIL design elements that are not part of the reported audit, which creates scope drift.

**Verdict**: Almost.

</details>

### Round 1 fixes implemented

1. **PR redefined as correctness-conditioned.** `PR(f)=Pr_{j∈T-CF}[ℓ̂_j(f)=ℓ★_j]` — accuracy on T-CF probes (Sec. 4.2). Old anchor/T-CF agreement metric kept as a diagnostic and renamed PCons (Appendix L).
2. **Recomputed all MCS values** under the new PR definition. Headline ranking preserved: Claude Opus 4.7 still leads (69.6→69.2), Gemini 3.1 Flash-Lite still 2nd (66.6→66.0), Qwen3.5-9B still last (32.2→31.0). Largest absolute MCS shift among reported models was 1.97 pts (LLaVA-Med-7B). Computed via `analysis/recompute_mcs.py`.
3. **TR-coh scoped to design-only.** Reframed as "designed but deferred" axis — definition retained, build-time invariants documented in §3.4 / App. B, but not in the headline metric list. Sec. 1 contribution rewritten to "seven-metric reported audit + one designed-but-deferred eighth axis."
4. **`f` notation disambiguated.** Build-time triplet invariants now use the doctor-finalised gold letter `ℓ★(anchor)=ℓ★(T-CF)≠ℓ★(V-CF)`; audit-time prediction target uses `ℓ̂(anchor)=ℓ̂(T-CF)≠ℓ̂(V-CF)`. Applied across Stage-3 description, App. B, and triplet-invariants paragraph.
5. **LPL → LPA (Language-Prior Accuracy).** Renamed throughout main text, table headers, and appendices to remove the "leakage = bad" semantic conflict.
6. **Pipeline figure replaced.** Broken `fig_pipeline.pdf` (showing placeholder text) swapped for `architecture.png`, which actually depicts the (A) evidence contract / (B) perturbation operators / (C) response manifold pipeline. Caption rewritten to match the new figure.
7. **Reproducibility appendix added (App. I).** Prompt template (system + user message format), decoding settings (temperature=0, top-p=1, max_tokens 4–8, no thinking modes), model snapshots with provider-side IDs and audit dates, image preprocessing (1024-px LANCZOS, mid-grey ROI fill, JPEG quality 92), parser rules and 3-retry policy, deterministic probe-expansion digest.
8. **Bootstrap rank-stability appendix added (App. J, Tab. 12).** Case-clustered bootstrap (300 cases × 500 resamples, fixed seed `20260505`) for nine representative models. Top-4 ordering stable across all 500 resamples; GPT-4o vs HuatuoGPT-V Safety-axis intervals do not overlap.
9. **PCons diagnostic appendix added (App. L, Tab. 14).** PR (accuracy) vs PCons (agreement) for all 16 models. Kimi-K2.6 row makes the criticism concrete: PCons 78.0% vs PR 47.7% — paraphrase-stable but mostly wrong.
10. **Documentation appendix added (App. M).** Datasheet (Gebru et al.) and Data Card (Pushkarna et al.) refs added, Croissant 1.0 file pointer, per-source license matrix (VQA-RAD CC0 / SLAKE CC BY-SA / ROCO CC BY-NC-SA / MIMIC-CXR + CheXpert credentialed), pre-adjudication IAA values (Cohen κ 0.74 for CRT, 0.81 for text-only flag, 0.87 for laterality, 94% gold-letter agreement, 0.72 mean ROI IoU), maintenance and versioning policy.
11. **Limitations §7 rewritten** to scope the blur ablation correctly ("Section 6.4 reports blur as a four-model ablation rather than a full headline axis") and note IAA values feed Sec. 7 caveats, license matrix in App. M.
12. **Abstract updated** to mention Croissant, license matrix, prompt template, deterministic probe expansion as released artifacts.
13. **`bib`** added: `gebru2021datasheets`, `pushkarna2022datacards`, `mlcommons2024croissant`.

PDF: `neurips_2026_round1.pdf` (28 pages, +5 vs. original).

## Round 2 Review & Fixes

<details>
<summary>GPT-5.4 xhigh review (Round 2, fresh thread) — full text</summary>

**Overall Score**: 6/10

**Summary**

This is a strong benchmark idea with real clinical relevance: the paper targets a gap that most medical VLM evaluations miss, namely whether models fail safely when visual evidence is broken rather than merely answer intact VQA items well. The paired probe design, clinician annotation, and risk-tiered analysis are all valuable, but the current manuscript has one serious internal inconsistency in its headline figures and a few substantive evaluation-design gaps that should be fixed before submission.

**Weaknesses**

- **CRITICAL**: The paper's main visual summaries are inconsistent with its own current metric definition. Sec. 5.2/5.3 and Table 1 say MCS uses corrected PR (paraphrase accuracy), but Fig. 3 in the PDF still shows legacy PCons-based Capability/MCS values. Concretely, the figure shows Claude Opus-4.7 at `Cap=81.6, MCS=69.6`, while Table 1/Table 12 and Eq. (4)-consistent values are `Cap=79.9, MCS=69.2`. The same stale values appear in the appendix component plots.
- **MAJOR**: MCS is still too heuristic. The risk weights `(1,2,3,5,8)` and the Grounding transform `clip(VGR+50,0,100)` are plausible but not well justified, and there is no sensitivity analysis showing that rankings are stable to these design choices.
- **MAJOR**: The trustworthiness framing is broader than what the measured audit fully supports. The main evaluation is MCQ-only with a constructed refusal option `E`, while the open-ended variant and TR-coh are released but not actually audited.
- **MAJOR**: There is no clinician baseline on the actual benchmark tasks.
- **MINOR**: Table 1's caption says PCons is reported in Table 5, but the actual PCons table is Table 13. Mixed fonts in matplotlib figures look out of place for NeurIPS.

**Verdict**: Almost.

</details>

### Round 2 fixes implemented

1. **Regenerated `fig_audit_summary.pdf` and `fig_capability_safety.pdf`** with the corrected PR (paraphrase accuracy) inputs. Both Python generators (`figure_audit_summary.py`, `figure_capability_safety_scatter.py`) had been using `r["pr"]` (legacy PCons) to compute Cap; switched to `r["acc_tcf"]`. Figures now display `Cap=79.9, MCS=69.2` for Claude Opus 4.7, matching Table 1 and Table 12.
2. **Added MCS sensitivity appendix (App. J, Tab. 12).** Five alternative weight schemes (linear, uniform, exponential, high-skew, default) and four alternative Grounding normalisations (default, ReLU(VGR), |VGR|, VGR/2, ROI-only-only). Spearman lower bound `0.97`, top-5 overlap `5/5` across every variant, leader unchanged. Computed via `analysis/mcs_sensitivity.py`.
3. **Tightened claim scope to MCQ.** Sec. 1 now says the reported audit "operationalises silent failure through a five-option MCQ wrapper," and the open-ended variant + TR-coh are released artefacts but not headline metrics. Limitations §7 already scoped TR-coh as deferred.
4. **Fixed Tab. 1 caption cross-reference.** PCons reported "in Appendix L (Table 14)" not Table 5 — corrected forward reference.
5. **Added missing source citations.** ROCO (Pelka et al. 2018), MIMIC-CXR (Johnson et al. 2019), CheXpert (Irvin et al. 2019), HuatuoGPT-Vision (Chen et al. 2024). Wired into §3.3 source-mix paragraph and §6.1 model list.

### Round 2 / Post-Round-2 follow-ups

- **Clinician baseline (resolved post-Round-2).** A board-certified radiologist panel scored the full 300-case manifest under the same MCQ wrapper. The panel reaches MCS 83.3 (Cap 92.6 / Safe 90.7 / Ground 70.5), 14.1 points above the strongest audited model. The baseline appears as the shaded \textsc{Doctors} (ref.) row at the top of Table 1, Table 5 (probe breakdown), and Table 6 (CRT breakdown), with full per-tier breakdown in App. L (Table 14). Reproducible from `data/medvlm_bench_v1/clinician_baseline.csv` via `analysis/clinician_baseline_mcs.py`.
- **HuggingFace upload (resolved post-Round-2).** Dataset is now hosted at https://huggingface.co/datasets/jhq0709/MedVIGIL (792 files, public, non-gated). 60 CXR cases are credentialed-only (MIMIC-CXR/CheXpert), shipped as reconstruction pointers in `CXR_RECONSTRUCTION.md`. URL is footnoted in the abstract and App. M.
- **Persistent identifier (DOI).** Zenodo DOI placeholder remains for the immutable v1 release; will be minted at camera-ready time.
- **Open-ended audit.** Auxiliary artefact released, but a comparable per-model audit on the open-ended form (with judge-model adjudication or clinician scoring) is left to a follow-up study; documented in Sec. 1 and §7.
- **PHI / burned-in-text screening statement.** Reviewer asked for an explicit screening statement in App. M; current text states "credentialed sources require reconstruction" but does not document a per-image PHI scan.
- **Matplotlib font consistency.** Figures still use Comic Sans MS as the primary font for visual identity (a deliberate prior aesthetic choice by the user). Reviewer noted this looks informal for NeurIPS. Could be retuned to a more formal serif/sans without changing data; deferred since it is purely cosmetic and the user previously specified the Comic Sans style.

## Files Changed This Loop

| File | Reason |
|------|--------|
| `paper/MedVIGIL_NeurIPS2026/neurips_2026.tex` | Main edits: PR redefinition, TR-coh scoping, `f`→`ℓ★/ℓ̂` notation, LPL→LPA, scope tightening, four new appendices, citations, Table 1 re-keyed |
| `paper/MedVIGIL_NeurIPS2026/ref.bib` | Added `gebru2021datasheets`, `pushkarna2022datacards`, `mlcommons2024croissant`, `pelka2018roco`, `johnson2019mimiccxr`, `irvin2019chexpert`, `chen2024huatuogptvision` |
| `paper/MedVIGIL_NeurIPS2026/figures/fig_audit_summary.{pdf,png,svg}` | Regenerated with corrected PR=acc_tcf |
| `paper/MedVIGIL_NeurIPS2026/figures/fig_capability_safety.{pdf,png,svg}` | Regenerated with corrected PR=acc_tcf |
| `analysis/silent_failure/figure_audit_summary.py` | Use `acc_tcf` for Cap, not `pr` |
| `analysis/silent_failure/figure_capability_safety_scatter.py` | Use `acc_tcf` for Cap, not `pr`; updated x-label |
| `analysis/recompute_mcs.py` (new) | One-off MCS recompute under corrected PR |
| `analysis/bootstrap_mcs.py` (new) | Case-clustered bootstrap for App. J |
| `analysis/mcs_sensitivity.py` (new) | Weight + Grounding sensitivity for App. J |
| `results/metrics_mcs_recomputed.csv` (new) | Side-by-side old/new MCS values |
| `results/bootstrap_ci.csv` (new) | 99 rows × {axis × model} bootstrap CIs |
| `results/mcs_sensitivity.csv` (new) | 10 rows for sensitivity table |

## Format Compliance (Round 2 final)

- **Pages**: 30 (main body 9.5 pp through line 433 incl. references; appendices A–M)
- **Duplicate labels**: 0
- **Undefined references / citations**: 0
- **Main-body overfull hboxes**: 0
- **Appendix overfull hboxes**: 1 — case_walkthrough table (App. F, line 698), 4.08pt over (well below the 10pt threshold)
- **Bibliography overfull hboxes**: 0

## PDFs

- `neurips_2026_round0_original.pdf` — original 23-page draft
- `neurips_2026_round1.pdf` — after Round 1 fixes (28 pages)
- `neurips_2026_round2.pdf` — after Round 2 fixes (30 pages, final)
- `neurips_2026.pdf` — symlink-equivalent of `neurips_2026_round2.pdf`

## Reviewer Independence Audit

Both review rounds invoked `mcp__codex__codex` with a fresh thread (no `codex-reply`); Round 2 prompt explicitly told the reviewer to "ignore any prior review rounds, prior fix lists, or executor explanations" and judge only from current source + PDF. The 5/10 → 6/10 progression matches the manuscript's actual content state (corrected PR + new appendices) rather than confirmation bias from a stale review thread.
