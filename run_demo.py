"""Run the text-only synthetic demonstration with Python's standard library."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_materials import check
from gate_demo import read_jsonl, replay
from metric_summary import aggregate, read_labels


def main():
    checks = check(ROOT)
    gates = replay(read_jsonl(ROOT / "examples" / "trajectories.jsonl"))
    metrics = aggregate(read_labels(ROOT / "examples" / "labels.csv"))
    output = ROOT / "demo_output"
    output.mkdir(exist_ok=True)
    for name, value in (("material_checks.json", checks), ("gate_decisions.json", gates),
                        ("metric_summary.json", metrics)):
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Synthetic demonstration only; no model calls and no network operations.")
    print("N={N}, N_T={N_T}; ACPR={acpr}%, TRR={trr}%, CDR={cdr}%".format(
        N=metrics["N"], N_T=metrics["N_T"], acpr=metrics["final_report_rates"]["ACPR"]["percentage"],
        trr=metrics["revision_rates"]["TRR"]["percentage"], cdr=metrics["revision_rates"]["CDR"]["percentage"]))
    print("Saved local checks and computed outputs in demo_output/.")


if __name__ == "__main__":
    main()
