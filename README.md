# FieldGuard supplementary materials

Repository: [https://github.com/weizhengju1004/fieldguard-reproducibility](https://github.com/weizhengju1004/fieldguard-reproducibility)

**Synthetic demonstration. All eight evidence snapshots, reports, feedback items, annotations and scoring labels are manually authored examples. No CLIP/Qwen inference or human-rating study was performed for this package. The publication status and any verified repository URL are recorded in `manifest.json`.**

This package follows the metric and gate definitions in the 2026-10-11 manuscript with unified figure typography. It demonstrates an evidence interface, prompt constraints, acceptance decisions and per-report arithmetic. It does not reproduce or validate the manuscript's performance tables. See `README_中文.md` for the Chinese guide.

## Contents

- `schemas/evidence.schema.json` and `docs/evidence_format.md`: proposed evidence serialization, units and empty-mask conventions.
- `prompts/`: p0, targeted p1 and generic-revision control templates, not recovered execution prompts.
- `docs/audit_rules.md`: extraction requirements, online audit and gate equations.
- `docs/metric_definitions.md`: independent evaluation references, joint passing, repair/damage counting and rounding.
- `examples/`: eight synthetic trajectories, full readable reports, distinct offline annotations and a binary-label CSV.
- `scripts/`: standard-library format checks, gate replay and label aggregation.
- `tests/`: counting and acceptance regression checks.
- `demo_output/`: results actually computed from this small authored demonstration.
- `manifest.json`, `VERIFICATION.json` and `SHA256SUMS.txt`: scope, local verification and integrity information.

## Run locally

Python 3.9+ is sufficient. Python 3.9.13 was used for local verification. No third-party Python dependencies, model weights, GPU or network access are needed by the demo. From the package directory:

```text
python -B run_demo.py
python -B -m unittest discover -s tests -v
```

The runner updates three JSON files in `demo_output/`. Individual commands:

```text
python -B scripts/metric_summary.py examples/labels.csv --output demo_output/metric_summary.json
python -B scripts/gate_demo.py examples/trajectories.jsonl --output demo_output/gate_decisions.json
```

The metric CLI uses its input manifest's denominators. The eight examples have `N=8` and `N_T=6`, not the manuscript's `N=1725` and `N_T=1112`. Their final ACPR is `3/8=37.5%`, TRR is `4/6=66.7%`, and CDR is `1/6=16.7%`. These are illustration results only.

## Scope of reproduction

Online q labels and independent offline y labels are supplied, authored inputs. The gate script applies the acceptance equations to q; the metric script aggregates y. Neither implements a complete natural-language extractor or semantic reviewer. A mention of a keyword is insufficient to establish criterion passing.

Offline labels and reference information must not enter online feedback. The synthetic offline annotations are stored separately. The examples include evidence-location error propagation, a false-normal decision, fallback, human referral and one deliberately simulated audit miss. None is an observed model failure or measured failure frequency.

The schema is a proposed public representation of the manuscript fields, not a recovered production schema. Checkpoint versions and visual assets remain null in the authored examples. No actual photos, heatmaps, public-dataset images, hidden model calls, real execution logs or reviewer identities are included.

The reproduction scope is method documentation, gate replay and metric aggregation from supplied labels. Empirical replication of the performance tables requires genuine inputs, inference records and independently obtained evaluation labels.
