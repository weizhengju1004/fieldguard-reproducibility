"""Counting and acceptance regressions; no model inference or human scoring."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from metric_summary import CRITERIA, aggregate, percentage, read_labels
from gate_demo import decide
from check_materials import grid_cell, validate_evidence


def row(sample_id="toy", initial=None, final=None, triggered="1",
        route="accept_r1", version="R1"):
    initial = initial or {k: 1 for k in CRITERIA}
    final = final or {k: 1 for k in CRITERIA}
    result = {"sample_id": sample_id, "data_status": "synthetic_authored",
              "triggered": triggered, "output_route": route,
              "metric_version": version}
    for key in CRITERIA:
        result["R0_" + key] = str(initial[key])
        result["FINAL_" + key] = str(final[key])
    return result


class MetricTests(unittest.TestCase):
    def test_full_authored_example_has_known_counts(self):
        rows = read_labels(ROOT / "examples" / "labels.csv")
        result = aggregate(rows)
        self.assertEqual(result["N"], 8)
        self.assertEqual(result["N_T"], 6)
        expected = {"DPR": 7, "LPR": 5, "GPR": 8, "SPR": 8,
                    "APR": 8, "CPR": 7, "EBR": 6, "ACPR": 3}
        for key, count in expected.items():
            self.assertEqual(result["final_report_rates"][key]["count"], count)
        self.assertEqual(result["revision_rates"]["TRR"]["count"], 4)
        self.assertEqual(result["revision_rates"]["CDR"]["count"], 1)
        self.assertEqual(result["repair_and_damage_overlap_count"], 1)

    def test_multiple_repairs_count_once_and_acpr_is_conjunction(self):
        before = {k: 1 for k in CRITERIA}
        before.update(SPR=0, APR=0)
        after = {k: 1 for k in CRITERIA}
        after["LPR"] = 0
        result = aggregate([row(initial=before, final=after)])
        self.assertEqual(result["revision_rates"]["TRR"]["count"], 1)
        self.assertEqual(result["revision_rates"]["CDR"]["count"], 1)
        self.assertEqual(result["final_report_rates"]["ACPR"]["count"], 0)

    def test_fallback_and_human_referral_remain_in_denominator(self):
        labels = {k: 1 for k in CRITERIA}
        labels["EBR"] = 0
        rows = [row("fallback", labels, labels, route="retain_r0", version="R0"),
                row("referral", labels, labels, route="human_review", version="R0")]
        result = aggregate(rows)
        self.assertEqual(result["N_T"], 2)
        self.assertEqual(result["revision_rates"]["TRR"]["count"], 0)
        self.assertEqual(result["revision_rates"]["CDR"]["count"], 0)
        self.assertEqual(result["final_report_rates"]["EBR"]["denominator"], 2)

    def test_unevaluable_is_failure_not_removed(self):
        candidate = row()
        candidate["FINAL_EBR"] = ""
        result = aggregate([candidate])
        self.assertEqual(result["N"], 1)
        self.assertEqual(result["final_report_rates"]["EBR"]["count"], 0)
        self.assertEqual(result["unevaluable_label_cells"], 1)

    def test_duplicates_and_inconsistent_fallback_are_rejected(self):
        with self.assertRaises(ValueError):
            aggregate([row(), row()])
        candidate = row(route="retain_r0", version="R0")
        candidate["FINAL_LPR"] = "0"
        with self.assertRaises(ValueError):
            aggregate([candidate])

    def test_no_triggered_records_has_undefined_revision_rates(self):
        result = aggregate([row(triggered="0", route="retain_r0", version="R0")])
        self.assertEqual(result["N_T"], 0)
        self.assertIsNone(result["revision_rates"]["TRR"]["percentage"])
        self.assertIsNone(result["revision_rates"]["CDR"]["percentage"])

    def test_round_after_counting_and_do_not_assume_paper_denominators(self):
        self.assertEqual(percentage(1, 16), 6.3)
        self.assertEqual(percentage(4, 6), 66.7)
        self.assertEqual(percentage(1428, 1725), 82.8)
        self.assertEqual(percentage(369, 1112), 33.2)


class GateTests(unittest.TestCase):
    def test_repair_with_new_error_is_rejected(self):
        q0 = {k: 1 for k in CRITERIA}
        q0["LPR"] = 0
        q1 = {k: 1 for k in CRITERIA}
        q1["SPR"] = 0
        result = decide(q0, q1, 0, 0)
        self.assertEqual(result["recognized_repairs"], 1)
        self.assertEqual(result["new_audited_errors"], 1)
        self.assertEqual(result["output_route"], "retain_r0")

    def test_some_repair_is_sufficient_but_critical_violation_is_not(self):
        q0 = {k: 1 for k in CRITERIA}
        q0.update(SPR=0, APR=0)
        q1 = deepcopy(q0)
        q1["SPR"] = 1
        self.assertTrue(decide(q0, q1, 0, 0)["accepted"])
        self.assertEqual(decide(q0, q1, 1, 1)["output_route"], "human_review")

    def test_untriggered_record_has_no_second_candidate(self):
        q0 = {k: 1 for k in CRITERIA}
        self.assertEqual(decide(q0, None, 0, None)["output_route"], "retain_r0")
        with self.assertRaises(ValueError):
            decide(q0, q0, 0, 0)


class EvidenceTests(unittest.TestCase):
    def test_internal_grid_boundaries_go_right_and_down(self):
        self.assertEqual(grid_cell([1 / 3, 0.2]), "upper-middle")
        self.assertEqual(grid_cell([2 / 3, 2 / 3]), "lower-right")
        self.assertEqual(grid_cell([1.0, 1.0]), "lower-right")

    def test_empty_mask_cannot_invent_a_numeric_area(self):
        import json
        evidence = json.loads((ROOT / "examples" / "evidence" / "demo-007.json").read_text(encoding="utf-8"))
        validate_evidence(evidence)
        evidence["region"]["area_fraction"] = 0
        with self.assertRaises(ValueError):
            validate_evidence(evidence)


if __name__ == "__main__":
    unittest.main()
