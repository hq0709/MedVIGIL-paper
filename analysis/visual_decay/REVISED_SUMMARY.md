# Revised visual-decay summary

`results/visual_decay_summary.csv` records the 32 percentages from the
author-edited Table 16 on 2026-10-18. It is a reported-accuracy summary, not
new inference output. No integer counts, denominators or tier values have
been inferred from those rounded percentages. Drop is calculated from the
reported clean and no-image percentages; L* uses the same reported curves.

The existing `results/blur_aggregate.csv` is preserved unchanged. It covers
300 original probes: 296 image-required and 4 text-answerable (all L1).
Its image-required tier sizes are 67, 31, 118, 43 and 37. Some of its weighted
tier averages disagree with the revised Table 16. The author corrected Huatuo no-image accuracy to 20.7% on 2026-10-18.
Its drop is 34.6 percentage points under the displayed-percentage convention;
L* remains 32. The author chose to retain the current Figure 6 as a
separate analysis of the original 296-case image-required subset. Its
caption and discussion state that scope explicitly; no replacement
tier values are inferred from the revised overall percentages.

Regenerate the revised overall Figure 4 with:

```text
python analysis/visual_decay/figure_visual_decay.py --skip-per-tier
```

The dashed text-answerable reference is unchanged from the existing
count-based file (n=4). It is not assumed to remain constant at every blur.
The `--skip-per-tier` mode writes only the four overall rows to the
crossover CSV and leaves Figure 6 unchanged. It does not mix old tier rows
into the revised crossover summary.

To regenerate Figure 6 as a decomposition of the revised overall results,
supply the actual revised tier records using `--aggregate PATH`. Without
`--skip-per-tier`, the script validates every weighted tier average against
the revised summary before generating either figure. It refuses to portray
inconsistent old tiers as a decomposition of the new overall percentages.
