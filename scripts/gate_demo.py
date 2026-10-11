"""Replay the manuscript gate from authored audit labels, not from report text."""
import argparse
import json
from pathlib import Path
from metric_summary import CRITERIA


def read_jsonl(path):
    records = []
    with Path(path).open("r", encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError("Invalid JSON on line " + str(number)) from exc
    return records


def audit_labels(labels):
    if not isinstance(labels, dict) or set(labels) != set(CRITERIA):
        raise ValueError("Audit labels must contain exactly the seven criteria.")
    if any(type(value) is not int or value not in (0, 1) for value in labels.values()):
        raise ValueError("Audit labels must be integer zero or one.")


def critical_count(value):
    if type(value) is not int or value < 0:
        raise ValueError("Critical violation counts must be nonnegative integers.")


def decide(q0, q1, h0, h1):
    audit_labels(q0)
    critical_count(h0)
    targets = [key for key in CRITERIA if q0[key] == 0]
    triggered = bool(targets)
    if not triggered and (q1 is not None or h1 is not None):
        raise ValueError("Untriggered records cannot have a second candidate.")
    if not triggered and h0:
        raise ValueError("A critical failure must also fail an audited criterion.")
    if q1 is None:
        if h1 is not None:
            raise ValueError("A missing candidate cannot have candidate audit results.")
        repairs = new_errors = 0
        accepted = False
    else:
        audit_labels(q1)
        critical_count(h1)
        repairs = sum(q1[key] for key in targets)
        new_errors = sum(q0[key] * (1 - q1[key]) for key in CRITERIA)
        accepted = bool(triggered and repairs > 0 and new_errors == 0 and h1 == 0)
    route = "accept_r1" if accepted else ("retain_r0" if h0 == 0 else "human_review")
    return {"triggered": triggered, "targets": targets, "recognized_repairs": repairs,
            "new_audited_errors": new_errors, "accepted": accepted,
            "output_route": route,
            "retained_version": "R1" if accepted else ("R0" if h0 == 0 else None)}


def replay(cases):
    decisions, seen = [], set()
    for case in cases:
        sid = case["sample_id"]
        if sid in seen:
            raise ValueError("Duplicate case identifier.")
        seen.add(sid)
        initial, revision = case["R0"], case["R1"]
        result = decide(initial["online_audit"], revision["online_audit"] if revision else None,
                        initial["critical_violations"], revision["critical_violations"] if revision else None)
        result["sample_id"] = sid
        decisions.append(result)
    return {"result_status": "gate_replay_from_synthetic_authored_labels",
            "scope": "No natural-language audit, model inference or offline truth is used.",
            "decisions": decisions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trajectories_jsonl", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload = json.dumps(replay(read_jsonl(args.trajectories_jsonl)), indent=2) + "\n"
        if args.output:
            if args.output.resolve() == args.trajectories_jsonl.resolve():
                raise ValueError("Output must not overwrite input trajectories.")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
            print("Wrote gate decisions from synthetic authored labels.")
        else:
            print(payload, end="")
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
