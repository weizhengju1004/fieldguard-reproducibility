# Independent metrics and counting / 指标与计数

Status: definitions from the latest manuscript. Supplied y labels are authored illustrations. `metric_summary.py` aggregates those labels; it does not verify their semantics or source annotations.

## Binary passing criteria

Set y=1 only when the complete criterion passes; otherwise y=0. Required missing, contradictory, unparseable or unevaluable statements fail. Equivalent phrasing is allowed with negation and uncertainty checked in context.

| Criterion | Offline reference and complete condition |
|---|---|
| DPR | Decision agrees with the independent public image label in an empirical evaluation |
| LPR | Asserted principal location agrees with the principal ground-truth component's 3×3 cell, with no conflicting or invented locations; a normal report explicitly states no defect location |
| GPR | Visual grade matches E after frozen synonym normalization |
| SPR | Absolute score error ≤0.005 on `[0,1]` |
| APR | Absolute area-fraction error ≤0.002, equivalent to 0.2 percentage points; an empty detector mask requires explicit not applicable |
| CPR | For anomalous images, actual statements cover appearance, location, impact, cause and inspection action; justified unknowns can satisfy a topic. Normal reports state no visible anomaly and the observation scope |
| EBR | Evaluable text contains no unsupported definite cause/impact, unjustified high-risk intervention or unrelated recommendation |

Only DPR/LPR measure agreement with independent image annotations. GPR/SPR/APR measure faithful reproduction of detector fields. These meanings must remain distinct when E is wrong. CPR/EBR require contextual interpretation rather than isolated keyword matching.

The demonstration's `offline_annotations.jsonl` is manually authored, not the public dataset's labels or masks. In `demo-006`, E says lower-left while the constructed offline location is upper-right. An E-consistent accepted revision still fails offline LPR. In `demo-007`, the constructed anomalous image receives a normal E decision; faithful reporting can fail offline DPR/LPR/CPR.

## Report rates and ACPR

```text
PR_j = 100 * sum(y_i,j) / N
ACPR = 100 * sum(all(y_i,j == 1 for j in the seven criteria)) / N
```

Each numerator counts reports, not mentions or correct phrases. ACPR requires all seven criteria on the same report and is not the mean of the seven rates. All required manifest records remain in N.

## TRR and CDR

Freeze the trigger set from the original online R0 audit. From offline R0 labels, U contains initially failed criteria and V initially passed criteria. Compare with the final chosen model text's offline labels:

```text
repair_i = any(y_final[i,j] == 1 for j in U_i)
damage_i = any(y_final[i,j] == 0 for j in V_i)
TRR = 100 * sum(repair_i for i in the fixed trigger set) / N_T
CDR = 100 * sum(damage_i for i in the fixed trigger set) / N_T
```

A report can repair several fields and contributes once to TRR. Repair and damage may coexist and both count. Evaluate the retained R1, or R0 on fallback; a rejected candidate's repair/damage does not contribute. Fallback to unchanged R0 contributes neither. Untriggered records retain R0 and do not enter the revision-rate numerators or denominator.

Human-referral records remain in N and N_T as applicable. Use explicitly specified pre-handover model text without human edits. `demo-005` specifies R0 for this purpose while the gate's retained output is null; this distinction does not turn the rejected text into an accepted report. An unevaluable criterion receives 0 and does not remove the record. If later supplying actual results, define the pre-handover model-text policy before scoring and keep it fixed.

For A4, compare the final chosen text against the original R0 over the original trigger set. M0/A3 have no revision rates. This material package includes neither these model runs nor additional revision rounds.

## Manifest, CSV and rounding

The current manuscript uses N=1725 and N_T=1112. This small demonstration uses N=8 and N_T=6. The script derives both denominators from its input CSV and does not manufacture missing rows to reach the manuscript totals. A zero trigger denominator yields null revision percentages, not a claimed 0% rate.

CSV columns are `sample_id`, `data_status`, binary `triggered`, `output_route`, `metric_version`, and seven `R0_` plus seven `FINAL_` labels. A blank required label is unevaluable and counts as 0; a missing required column, duplicate identifier, invalid label or inconsistent R0 fallback is an error. Allowed model versions are R0/R1, so human-edited text is not an evaluation source here.

Count integers first, then round percentages to one decimal using decimal half-up. In this demonstration, ACPR=3/8=37.5%, TRR=4/6=66.7%, and CDR=1/6=16.7%. The repaired-and-damaged overlap is one record. These illustration results are unrelated to the locked manuscript table results.
