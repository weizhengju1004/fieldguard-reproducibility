# Online audit and gate / 在线审计与安全门

Status: specification aligned with the latest manuscript. The executable demo consumes hand-authored q labels; it does not implement the full natural-language extraction or contextual judgment described below.

## Field extraction requirements

Freeze keyword and synonym rules before comparison. Extract decision, asserted location, grade and engineering statements, and parse score and area into common units. Example equivalents include `upper-right` / `top-right`, `normal` / `no visible anomaly`, and fraction `0.036` / percentage `3.6%`.

These are examples of normalization, not an exhaustive recovered dictionary. Preserve negation, scope and qualifiers: “no anomaly in the upper-right” does not assert an anomaly there. “Possible contact damage” does not assert a confirmed cause. A standalone topic word does not satisfy a required statement. Ambiguous causal, impact or action claims require contextual semantic assessment; the demo does not automate it.

Assign required fields a state of `consistent`, `missing`, `conflicting` or `unparseable`. A complete accepted criterion receives q=1; failed required criteria receive q=0. Feedback identifies its field, observed problem, E-derived expected value or fixed rule, and requested correction without adding process facts.

The seven online axes use the same short names as the diagnostic rates, but their reference sources differ:

| Axis | Online reference |
|---|---|
| DPR | Fixed decision in E |
| LPR | Fixed location in E; explicit inapplicability when no candidate region exists |
| GPR | Fixed visual grade in E, with a frozen synonym mapping |
| SPR | E score, absolute error at most 0.005 on `[0,1]` |
| APR | E area fraction, absolute error at most 0.002; explicit not applicable for an empty mask |
| CPR | Required actual topic statements; the online normal/anomalous branch follows E |
| EBR | Claim support, qualifiers, evaluability and action relevance under reporting rules |

Online DPR/LPR cannot determine that a detector is correct against independent labels. Public image labels, ground-truth masks and reference reports must not appear in F or sample-specific generation instructions.

## Trigger and acceptance

Let J be the initially failed online criteria. Trigger if J is nonempty. The same I/H/E is supplied to the single targeted revision call with R0 and F. Untriggered records retain R0.

For a candidate R1, count recognized repairs and newly failed audited fields:

```text
u = sum(q1[j] for j in J)
v = sum(q0[j] * (1 - q1[j]) for j in the seven criteria)
accept = triggered AND (u > 0) AND (v == 0) AND (h1 == 0)
```

h counts critical violations, including an unparseable report. Unsupported unqualified diagnoses used to justify a high-risk intervention are a critical violation in the corresponding demonstration. A critical failure must also fail a relevant audit criterion.

Accept R1 if the condition holds. Otherwise retain R0 if h0=0; otherwise refer for human review. The gate requires at least one recognized repair, not repair of every failed field. It checks q and h, not offline y.

`demo-008` deliberately supplies q that miss a newly introduced unsupported definite cause. Independent y mark EBR failed. This constructed discrepancy demonstrates why internal acceptance cannot guarantee zero offline collateral damage; it does not claim a tested extractor made this mistake.
