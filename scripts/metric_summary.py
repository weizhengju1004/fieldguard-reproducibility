"""Aggregate supplied binary labels. Does not score report text or run models."""
import argparse
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CRITERIA = ("DPR", "LPR", "GPR", "SPR", "APR", "CPR", "EBR")
BASE_COLUMNS = ("sample_id", "data_status", "triggered", "output_route", "metric_version")
LABEL_COLUMNS = tuple(prefix + key for prefix in ("R0_", "FINAL_") for key in CRITERIA)


def percentage(count, denominator):
    if denominator == 0:
        return None
    if not 0 <= count <= denominator:
        raise ValueError("Count must be between zero and its denominator.")
    return float((Decimal(count) * 100 / Decimal(denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP))


def binary(value, allow_empty=False):
    if type(value) is int and value in (0, 1):
        return value
    if isinstance(value, str) and value in ("0", "1"):
        return int(value)
    if allow_empty and value == "":
        return 0
    raise ValueError("Labels and trigger flags must be 0 or 1; blank labels count as failures.")


def read_labels(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = set(BASE_COLUMNS + LABEL_COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        return list(reader)


def aggregate(rows):
    rows = list(rows)
    if not rows:
        raise ValueError("An empty manifest cannot define report rates.")
    counts0 = {k: 0 for k in CRITERIA}
    counts = {k: 0 for k in CRITERIA}
    n_triggered = repaired = damaged = overlap = joint0 = joint = missing_cells = 0
    seen, statuses, events = set(), set(), []
    routes = {"accept_r1": 0, "retain_r0": 0, "human_review": 0}
    for entry in rows:
        missing = set(BASE_COLUMNS + LABEL_COLUMNS) - set(entry)
        if missing:
            raise ValueError("Missing row columns: " + ", ".join(sorted(missing)))
        sid = entry["sample_id"]
        if not isinstance(sid, str) or not sid.strip() or sid in seen:
            raise ValueError("Sample identifiers must be nonempty and unique.")
        seen.add(sid)
        status = entry["data_status"]
        if not isinstance(status, str) or not status.strip():
            raise ValueError("Every row must declare its data provenance/status.")
        statuses.add(status)
        triggered = binary(entry["triggered"])
        route, version = entry["output_route"], entry["metric_version"]
        if route not in routes or version not in ("R0", "R1"):
            raise ValueError("Use a declared output route and a pre-handover model version.")
        if route == "retain_r0" and version != "R0":
            raise ValueError("Fallback must use R0 for evaluation.")
        if route == "accept_r1" and (version != "R1" or not triggered):
            raise ValueError("An accepted revision must be triggered and evaluated as R1.")
        if not triggered and (route != "retain_r0" or version != "R0"):
            raise ValueError("Untriggered records must preserve R0.")
        y0 = {k: binary(entry["R0_" + k], True) for k in CRITERIA}
        yf = {k: binary(entry["FINAL_" + k], True) for k in CRITERIA}
        if version == "R0" and yf != y0:
            raise ValueError("R0 evaluation must preserve the original labels.")
        missing_cells += sum(entry[c] == "" for c in LABEL_COLUMNS)
        for key in CRITERIA:
            counts0[key] += y0[key]
            counts[key] += yf[key]
        joint0 += int(all(y0.values()))
        joint += int(all(yf.values()))
        repair = bool(triggered and any(y0[k] == 0 and yf[k] == 1 for k in CRITERIA))
        damage = bool(triggered and any(y0[k] == 1 and yf[k] == 0 for k in CRITERIA))
        n_triggered += triggered
        repaired += int(repair)
        damaged += int(damage)
        overlap += int(repair and damage)
        routes[route] += 1
        events.append({"sample_id": sid, "triggered": bool(triggered),
                       "repair": repair, "damage": damage, "metric_version": version})

    def rate(count, denominator):
        return {"count": count, "denominator": denominator,
                "percentage": percentage(count, denominator)}

    n = len(rows)
    counts0["ACPR"], counts["ACPR"] = joint0, joint
    return {
        "result_status": "aggregate_of_supplied_labels_not_empirical_verification",
        "input_data_statuses": sorted(statuses), "N": n, "N_T": n_triggered,
        "initial_report_rates": {k: rate(v, n) for k, v in counts0.items()},
        "final_report_rates": {k: rate(v, n) for k, v in counts.items()},
        "revision_rates": {"TRR": rate(repaired, n_triggered),
                           "CDR": rate(damaged, n_triggered)},
        "repair_and_damage_overlap_count": overlap, "output_routes": routes,
        "unevaluable_label_cells": missing_cells, "case_events": events,
        "rounding": "one decimal place, decimal half-up, after integer counting",
        "scope": "No detector/Qwen inference, reference annotation or semantic review is performed."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = aggregate(read_labels(args.labels_csv))
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            if args.output.resolve() == args.labels_csv.resolve():
                raise ValueError("Output must not overwrite input labels.")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
            print("Wrote a supplied-label summary; this is not empirical verification.")
        else:
            print(payload, end="")
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
