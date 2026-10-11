"""Check local format, synthetic provenance, feedback scope and trace consistency."""
import hashlib
import json
from pathlib import Path
from gate_demo import read_jsonl, replay
from metric_summary import aggregate, read_labels

CELLS = (("upper-left", "upper-middle", "upper-right"),
         ("middle-left", "center", "middle-right"),
         ("lower-left", "lower-middle", "lower-right"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return type(value) in (int, float) and 0 <= value <= 1


def grid_cell(centroid):
    x, y = centroid
    return CELLS[min(int(y * 3), 2)][min(int(x * 3), 2)]


def validate_evidence(evidence):
    """Domain checks for this demo; this is not a general JSON Schema interpreter."""
    require(evidence["schema_version"] == "1.0.0-demo", "Wrong demo schema version.")
    require(evidence["provenance"] == {"kind": "synthetic_authored", "model_inference_run": False},
            "Every evidence snapshot must disclose its synthetic provenance.")
    image = evidence["image"]
    for key in ("width_px", "height_px"):
        require(type(image[key]) is int and image[key] > 0, "Invalid image dimensions.")
    require(image["original_image_path"] is None and evidence["heatmap"]["path"] is None,
            "This text-only demonstration must not claim measured visual assets.")
    require(evidence["heatmap"]["normalized_range"] == [0, 1], "Wrong heatmap scale.")
    require(evidence["anomaly"]["decision"] in ("normal", "anomalous"), "Invalid decision.")
    require(number(evidence["anomaly"]["score"]), "Score is outside [0, 1].")
    require(evidence["versions"]["detector_checkpoint_revision"] is None,
            "No actual checkpoint is established for authored examples.")
    require(evidence["visual_grade"] in ("mild", "moderate", "marked", "not_applicable"),
            "Invalid demo grade vocabulary.")
    region = evidence["region"]
    require(type(region["mask_empty"]) is bool, "mask_empty must be boolean.")
    spatial = ("principal_component_id", "principal_centroid_normalized", "grid_location",
               "bounding_box_normalized", "area_fraction")
    if region["mask_empty"]:
        require(all(region[key] is None for key in spatial), "Empty-mask fields must be null.")
    else:
        area = region["area_fraction"]
        require(number(area) and area > 0, "Nonempty-mask area must be in (0, 1].")
        require(isinstance(region["principal_component_id"], str) and region["principal_component_id"],
                "Nonempty mask needs a principal component identifier.")
        centroid, box = region["principal_centroid_normalized"], region["bounding_box_normalized"]
        require(isinstance(centroid, list) and len(centroid) == 2 and all(number(v) for v in centroid),
                "Invalid normalized centroid.")
        require(isinstance(box, list) and len(box) == 4 and all(number(v) for v in box),
                "Invalid normalized bounding box.")
        require(box[0] < box[2] and box[1] < box[3], "Bounding-box bounds are reversed.")
        require(box[0] <= centroid[0] <= box[2] and box[1] <= centroid[1] <= box[3],
                "Principal centroid must lie inside its box.")
        require(region["grid_location"] == grid_cell(centroid), "Centroid/grid mapping disagrees.")


def check(root):
    root = Path(root).resolve()
    cases = read_jsonl(root / "examples" / "trajectories.jsonl")
    rows = read_labels(root / "examples" / "labels.csv")
    offline = read_jsonl(root / "examples" / "offline_annotations.jsonl")
    case_ids = [c["sample_id"] for c in cases]
    require(len(cases) == 8 and len(set(case_ids)) == 8, "Expected eight distinct demo cases.")
    require(set(case_ids) == {r["sample_id"] for r in rows}, "Case/label identifiers differ.")
    require(len(offline) == 8 and set(case_ids) == {r["sample_id"] for r in offline},
            "Case/offline-annotation identifiers differ.")
    require(all(r["annotation_status"] == "synthetic_authored_not_public_dataset_labels" for r in offline),
            "Offline annotations must disclose their authored status.")
    decisions = replay(cases)["decisions"]
    by_decision = {d["sample_id"]: d for d in decisions}
    by_row = {r["sample_id"]: r for r in rows}
    for case in cases:
        sid = case["sample_id"]
        require(case["data_status"] == "synthetic_authored", "Wrong trajectory data status.")
        relative = Path(case["evidence_file"])
        require(not relative.is_absolute() and ".." not in relative.parts, "Use a package-relative evidence path.")
        evidence_path = (root / relative).resolve()
        require(root in evidence_path.parents, "Evidence must stay inside the package.")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        require(evidence["sample_id"] == sid, "Evidence/case identifiers differ.")
        validate_evidence(evidence)
        fingerprint = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        for version in ("R0", "R1"):
            if case[version]:
                require(case[version]["evidence_sha256"] == fingerprint,
                        "The two authored report stages must reference the identical evidence bytes.")
                require(isinstance(case[version]["text"], str) and case[version]["text"].strip(), "Report text missing.")
        decision, row = by_decision[sid], by_row[sid]
        feedback = case["feedback"]
        require(set(feedback) == {"targets", "issues"}, "Unexpected online feedback fields.")
        require(feedback["targets"] == decision["targets"], "Feedback targets differ from initial failed audit fields.")
        require([issue["criterion"] for issue in feedback["issues"]] == decision["targets"], "Feedback issues are incomplete.")
        for issue in feedback["issues"]:
            require(set(issue) == {"criterion", "status", "observed", "expected_or_rule", "instruction"},
                    "Feedback contains an unexpected reference field.")
            require(issue["status"] in ("missing", "conflicting", "unparseable"), "Invalid failed-field status.")
        require(decision["output_route"] == case["expected_output_route"] == row["output_route"],
                "Recorded route differs from gate replay.")
        require(int(decision["triggered"]) == int(row["triggered"]), "Trigger manifest differs from gate replay.")
        require(case["metric_model_version"] == row["metric_version"], "Metric model versions disagree.")
        require(row["data_status"] == "synthetic_authored", "Missing CSV synthetic status.")
    summary = aggregate(rows)
    expected = json.loads((root / "examples" / "expected_metrics.json").read_text(encoding="utf-8"))
    require((summary["N"], summary["N_T"]) == (expected["N"], expected["N_T"]), "Wrong denominators.")
    for key, count in expected["final_counts"].items():
        require(summary["final_report_rates"][key]["count"] == count, "Wrong count for " + key)
    require(summary["revision_rates"]["TRR"]["count"] == expected["repair_count"], "Wrong repair count.")
    require(summary["revision_rates"]["CDR"]["count"] == expected["damage_count"], "Wrong damage count.")
    require(summary["repair_and_damage_overlap_count"] == expected["overlap_count"], "Wrong overlap count.")
    # Counterexample: feedback cannot import the authored offline location.
    wrong_case = next(c for c in cases if c["sample_id"] == "demo-006")
    require("upper-right" not in json.dumps(wrong_case["feedback"]), "Offline location leaked into feedback.")
    return {"verification_scope": "local_synthetic_format_and_arithmetic_only", "passed": True,
            "case_count": len(cases), "report_text_count": sum(1 + bool(c["R1"]) for c in cases),
            "evidence_fingerprints_reused": True, "synthetic_provenance_checked": True,
            "feedback_target_and_field_checks": True, "gate_and_evaluation_separation_checked": True,
            "authored_expected_counts_matched": True,
            "actual_detector_or_qwen_inference": False, "actual_image_or_heatmap_validation": False,
            "automatic_natural_language_or_semantic_scoring": False}


if __name__ == "__main__":
    print(json.dumps(check(Path(__file__).resolve().parents[1]), indent=2))
