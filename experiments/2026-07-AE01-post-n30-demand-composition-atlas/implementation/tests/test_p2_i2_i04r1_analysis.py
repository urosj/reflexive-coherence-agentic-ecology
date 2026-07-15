from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


def _find_repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        experiment = parent / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
        if (parent / ".git").exists() and experiment.is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_repository_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import ContractError  # noqa: E402
from p2_i2_i04r1_analysis import (  # noqa: E402
    analyze_mode_primary,
    classify_margin_panel,
    derive_causal_chain_status,
    evaluate_numeric_rule,
    evaluate_quantity_scope_diagnostic,
    normalized_paired_difference,
    primary_margin,
    validate_analysis_policy,
    validate_numeric_admissibility,
    validate_response_record,
)
from p2_i2_i04r1_calibration import validate_calibration_policy  # noqa: E402


class P2I2I04R1AnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.analysis = json.loads(
            (EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json").read_text()
        )
        cls.calibration = json.loads(
            (EXPERIMENT / "configs/p2_i2_i04r1_calibration_policy.json").read_text()
        )

    def _record(
        self,
        *,
        record_id: str,
        branch_id: str,
        response: float | None,
        status: str = "observed_response",
        mode: str = "state_carried",
        seed: int = 101,
        order: str = "q1_then_q2",
        carrier_digest: str | None = None,
        pairing_identity: str = "corrected-analysis-unit-pair",
    ) -> dict[str, object]:
        observed = status == "observed_response"
        no_response = status == "scientific_no_response"
        scientific = observed or no_response
        before = 10.0
        return {
            "record_id": record_id,
            "mode": mode,
            "seed": seed,
            "physical_order_id": order,
            "cell_id": "combined-orders" if branch_id == "combined-orders" else "unit-control",
            "branch_id": branch_id,
            "pairing_identity": pairing_identity,
            "opportunity_id": "analysis-unit-opportunity",
            "response_id": "fixed_window_native_B_target_coherence_gain",
            "unit": "native_coherence_amount",
            "status": status,
            "B_before": before,
            "B_after": before + float(response) if scientific else None,
            "raw_response": response,
            "oriented_response": response,
            "carrier_state_digest": carrier_digest or f"carrier-{record_id}",
            "window_protocol_id": "p2-i2-native-response-window-v2",
            "pre_packet_queue_length": 0,
            "pre_birth_queue_length": 0,
            "post_packet_queue_length": 0,
            "post_birth_queue_length": 0,
            "feedback_surface_call_count": 1 if scientific else 0,
            "producer_call_count": 1 if scientific else 0,
            "step_call_count": 2 if scientific else 1,
            "step_processed_event_kinds": (
                ["packet_departure", "packet_arrival"]
                if observed
                else ["event_queue_empty", "event_queue_empty"]
                if no_response
                else ["packet_departure"]
            ),
            "producer_reason": "scheduled" if observed else "no_event" if no_response else "exception",
            "response_packet_id": "packet-1" if observed else None,
            "departure_event_id": "departure-1" if observed else None,
            "arrival_event_id": "arrival-1" if observed else None,
            "response_packet_amount": response if observed else None,
            "runtime_tolerance": 0.0,
            "B_targeting_event_ids": ["arrival-1"] if observed else [],
            "native_chain_evidence_refs": ["producer-1", "departure-1", "arrival-1"]
            if observed
            else [],
            "operational_failure_id": None if scientific else "unit-operational-failure",
        }

    def _causal(self, kind: str = "candidate") -> dict[str, object]:
        return {
            "evidence_id": f"evidence-{kind}",
            "branch_id": f"branch-{kind}",
            "branch_kind": kind,
            "mode": "state_carried",
            "common_carrier_id": "P",
            "common_carrier_mask": ["P"],
            "private_partitions": [
                {"partition_id": "private-1", "member_ids": ["P1"]},
                {"partition_id": "private-2", "member_ids": ["P2"]},
            ],
            "contribution_arrivals": [
                {"source_role": "S1", "target_carrier_id": "P", "event_id": "q1-arrival"},
                {"source_role": "S2", "target_carrier_id": "P", "event_id": "q2-arrival"},
            ],
            "response_actor_id": "A",
            "response_target_id": "B",
            "response_front_masks": [{"actor_id": "A", "carrier_ids": ["P"]}],
            "call_records": [
                {
                    "phase": "response",
                    "actor": "A",
                    "callable": "pygrc.emit_feedback_eligibility_surface_row",
                    "input_carrier_ids": ["P", "B_ref"],
                }
            ],
            "producer_records": [
                {
                    "producer_record_id": "producer-1",
                    "feedback_row_id": "feedback-1",
                    "packet_id": "packet-1",
                }
            ],
            "packet_event_records": [
                {
                    "event_id": "departure-1",
                    "kind": "packet_departure",
                    "packet_id": "packet-1",
                    "source_id": "A",
                    "target_id": "B",
                },
                {
                    "event_id": "arrival-1",
                    "kind": "packet_arrival",
                    "packet_id": "packet-1",
                    "source_id": "A",
                    "target_id": "B",
                },
            ],
            "branch_configuration_sha256": "a" * 64,
            "runtime_binding_receipt_sha256": "b" * 64,
            "call_trace_sha256": "c" * 64,
        }

    def test_corrected_policies_validate_without_executing_null(self) -> None:
        validate_analysis_policy(self.analysis)
        validate_calibration_policy(self.calibration, self.analysis)

    def test_observed_and_complete_no_response_validate(self) -> None:
        validate_response_record(
            self._record(record_id="observed", branch_id="combined-orders", response=2.0)
        )
        validate_response_record(
            self._record(
                record_id="no-response",
                branch_id="combined-orders",
                response=0.0,
                status="scientific_no_response",
            )
        )

    def test_scheduled_but_incomplete_window_cannot_be_scientific_zero(self) -> None:
        record = self._record(
            record_id="incomplete",
            branch_id="combined-orders",
            response=0.0,
            status="scientific_no_response",
        )
        record["step_processed_event_kinds"] = ["packet_departure", "event_queue_empty"]
        with self.assertRaises(ContractError):
            validate_response_record(record)

    def test_operational_failure_requires_null_response(self) -> None:
        record = self._record(
            record_id="invalid",
            branch_id="combined-orders",
            response=None,
            status="invalid_window_protocol",
        )
        validate_response_record(record)
        record["raw_response"] = 0.0
        with self.assertRaises(ContractError):
            validate_response_record(record)

    def test_primary_uses_strongest_symmetric_leave_one(self) -> None:
        candidate = self._record(
            record_id="candidate", branch_id="combined-orders", response=4.0
        )
        q1_only = self._record(
            record_id="q1", branch_id="q1_admitted_q2_diverted", response=1.0
        )
        q2_only = self._record(
            record_id="q2", branch_id="q2_admitted_q1_diverted", response=2.0
        )
        result = primary_margin(candidate, q1_only, q2_only, self.analysis)
        self.assertEqual(result["selected_comparator_record_id"], "q2")
        self.assertEqual(result["strongest_leave_one_response"], 2.0)
        self.assertEqual(
            result["normalized_margin"], normalized_paired_difference(4.0, 2.0, 1e-12)
        )

    def test_primary_rejects_unchanged_carrier_or_pairing_drift(self) -> None:
        candidate = self._record(
            record_id="candidate",
            branch_id="combined-orders",
            response=4.0,
            carrier_digest="same",
        )
        q1_only = self._record(
            record_id="q1",
            branch_id="q1_admitted_q2_diverted",
            response=1.0,
            carrier_digest="same",
        )
        q2_only = self._record(
            record_id="q2", branch_id="q2_admitted_q1_diverted", response=2.0
        )
        with self.assertRaises(ContractError):
            primary_margin(candidate, q1_only, q2_only, self.analysis)
        q1_only["carrier_state_digest"] = "q1"
        q1_only["pairing_identity"] = "different"
        with self.assertRaises(ContractError):
            primary_margin(candidate, q1_only, q2_only, self.analysis)

    def test_relation_classifier_retains_all_direction_classes(self) -> None:
        self.assertEqual(classify_margin_panel([0.2, 0.3, 0.4], 0.1), "robust_aligned")
        self.assertEqual(classify_margin_panel([0.2, 0.0, 0.05], 0.1), "narrow_aligned")
        self.assertEqual(classify_margin_panel([0.2, -0.3, 0.0], 0.1), "mixed_direction")
        self.assertEqual(classify_margin_panel([0.0, 0.05, -0.05], 0.1), "resolution_limited")
        self.assertEqual(classify_margin_panel([None, 0.2], 0.1), "resolution_unknown")

    def test_common_numeric_controls_have_fail_closed_machine_rules(self) -> None:
        self.assertEqual(evaluate_numeric_rule("invariant", [0.01, -0.01], 0.1), "pass")
        self.assertEqual(evaluate_numeric_rule("different_unsigned", [0.2, -0.3], 0.1), "pass")
        self.assertEqual(evaluate_numeric_rule("different_unsigned", [0.2, 0.0], 0.1), "ambiguous")
        self.assertEqual(evaluate_numeric_rule("aligned_all", [0.2, 0.3], 0.1), "pass")
        self.assertEqual(
            evaluate_numeric_rule("access_relation_retained", [0.2, 0.3, 0.0], 0.1),
            "pass",
        )

    def test_mode_analysis_separates_order_conditioning_from_causal_failure(self) -> None:
        rows = []
        for order, values in (("q1_then_q2", [0.3, 0.4, 0.5]), ("q2_then_q1", [0.0, 0.0, 0.0])):
            rows.extend(
                {
                    "mode": "history_carried",
                    "seed": seed,
                    "physical_order_id": order,
                    "normalized_margin": value,
                }
                for seed, value in zip((101, 211, 307), values, strict=True)
            )
        result = analyze_mode_primary(
            "history_carried", rows, 0.1, op08_disposition="pass"
        )
        self.assertEqual(result["mode_metric_signature"], "order_conditioned_or_mixed")
        self.assertFalse(result["causal_failure_derived"])
        rows[0]["mode"] = "hybrid"
        with self.assertRaises(ContractError):
            analyze_mode_primary("history_carried", rows, 0.1, op08_disposition="pass")

    def test_top_signature_requires_both_order_panels(self) -> None:
        rows = [
            {
                "mode": "state_carried",
                "seed": seed,
                "physical_order_id": order,
                "normalized_margin": 0.5,
            }
            for order in ("q1_then_q2", "q2_then_q1")
            for seed in (101, 211, 307)
        ]
        result = analyze_mode_primary("state_carried", rows, 0.1, op08_disposition="pass")
        self.assertEqual(result["mode_metric_signature"], "top_aligned")

    def test_quantity_matched_equivalence_is_retained_without_R03_failure(self) -> None:
        candidate = self._record(
            record_id="candidate",
            branch_id="combined-orders",
            response=2.0,
            carrier_digest="complete-carrier",
        )
        repeated_s1 = self._record(
            record_id="repeated-s1",
            branch_id="quantity_matched_repeated_S1",
            response=2.0,
            carrier_digest="complete-carrier",
        )
        repeated_s2 = self._record(
            record_id="repeated-s2",
            branch_id="quantity_matched_repeated_S2",
            response=2.0,
            carrier_digest="complete-carrier",
        )
        result = evaluate_quantity_scope_diagnostic(
            candidate, repeated_s1, repeated_s2, 1e-12, self.analysis
        )
        self.assertEqual(result["scope_reading"], "source_label_invariant_equivalence")
        self.assertFalse(result["R03_failure"])
        self.assertEqual(set(result["normalized_margins"]), {"S1", "S2"})

    def test_I06_numeric_admissibility_separates_runtime_tolerance(self) -> None:
        admitted = validate_numeric_admissibility(10.0, 1e-6, 1e-12, self.analysis)
        self.assertTrue(admitted["admissible"])
        too_small = validate_numeric_admissibility(10.0, 1e-12, 0.0, self.analysis)
        self.assertFalse(too_small["admissible"])
        loose_runtime = validate_numeric_admissibility(10.0, 1e-6, 1e-7, self.analysis)
        self.assertFalse(loose_runtime["admissible"])

    def test_candidate_causal_status_is_derived_from_lineage(self) -> None:
        evidence = self._causal()
        result = derive_causal_chain_status(evidence)
        self.assertEqual(result["derived_status"], "valid_common_carrier")
        broken = deepcopy(evidence)
        broken["packet_event_records"][1]["target_id"] = "not-B"
        result = derive_causal_chain_status(broken)
        self.assertEqual(result["derived_status"], "invalid_common_carrier")

    def test_private_and_controller_exclusions_are_evidence_derived(self) -> None:
        private = self._causal("private_substitution")
        private["response_front_masks"] = [
            {"actor_id": "A1", "carrier_ids": ["P1"]},
            {"actor_id": "A2", "carrier_ids": ["P2"]},
        ]
        private["producer_records"] = []
        private["packet_event_records"] = []
        result = derive_causal_chain_status(private)
        self.assertEqual(result["derived_status"], "private_partition_excluded")

        controller = self._causal("controller_substitution")
        controller["call_records"][0]["callable"] = "controller.read_contributor_slots"
        controller["call_records"][0]["input_carrier_ids"] = ["S1", "S2"]
        result = derive_causal_chain_status(controller)
        self.assertEqual(result["derived_status"], "controller_bypass_excluded")

    def test_authored_causal_summary_boolean_is_rejected(self) -> None:
        evidence = self._causal()
        evidence["used_common_pool"] = True
        with self.assertRaises(ContractError):
            derive_causal_chain_status(evidence)


if __name__ == "__main__":
    unittest.main()
