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
from p2_i2_i04r2_analysis import (  # noqa: E402
    build_synthetic_response_envelope,
    primary_margin,
    validate_machine_policy,
    validate_response_envelope,
)
from p2_i2_i04r2_calibration import validate_calibration_policy  # noqa: E402


class P2I2I04R2AnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parent = json.loads(
            (EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json").read_text()
        )
        cls.machine = json.loads(
            (EXPERIMENT / "configs/p2_i2_i04r2_machine_policy.json").read_text()
        )
        cls.calibration = json.loads(
            (EXPERIMENT / "configs/p2_i2_i04r2_calibration_policy.json").read_text()
        )

    def _three_arms(self, *, response: float = 0.25) -> tuple[dict, dict, dict]:
        common = {
            "response": response,
            "seed": 19,
            "physical_order_id": "q1_then_q2",
            "pairing_identity": "i04r2-pure-unit-tuple",
        }
        candidate = build_synthetic_response_envelope(
            record_id="candidate",
            branch_id="combined-orders",
            carrier_state_digest="combined-carrier",
            **common,
        )
        q1_only = build_synthetic_response_envelope(
            record_id="q1-only",
            branch_id="q1_admitted_q2_diverted",
            carrier_state_digest="q1-carrier",
            **common,
        )
        q2_only = build_synthetic_response_envelope(
            record_id="q2-only",
            branch_id="q2_admitted_q1_diverted",
            carrier_state_digest="q2-carrier",
            **common,
        )
        return candidate, q1_only, q2_only

    def test_overlay_and_future_calibration_policies_validate_without_null_execution(self) -> None:
        validate_machine_policy(self.machine, self.parent)
        validate_calibration_policy(self.calibration, self.machine, self.parent)

    def test_complete_three_arm_tuple_uses_within_tuple_max(self) -> None:
        candidate, q1_only, q2_only = self._three_arms()
        q1_only["i04r1_response_record"]["B_after"] = 0.125
        q1_only["i04r1_response_record"]["raw_response"] = 0.125
        q1_only["i04r1_response_record"]["oriented_response"] = 0.125
        q1_only["i04r1_response_record"]["response_packet_amount"] = 0.125
        q1_only["arrival_gain_receipt"]["expected_native_arrival_gain"] = 0.125
        q2_only["i04r1_response_record"]["B_after"] = 0.2
        q2_only["i04r1_response_record"]["raw_response"] = 0.2
        q2_only["i04r1_response_record"]["oriented_response"] = 0.2
        q2_only["i04r1_response_record"]["response_packet_amount"] = 0.2
        q2_only["arrival_gain_receipt"]["expected_native_arrival_gain"] = 0.2
        result = primary_margin(candidate, q1_only, q2_only, self.machine, self.parent)
        self.assertTrue(result["complete_three_arm_tuple_valid"])
        self.assertEqual(result["selected_comparator_record_id"], "q2-only")
        self.assertEqual(result["strongest_leave_one_response"], 0.2)

    def test_one_invalid_leave_arm_makes_tuple_nonevaluable(self) -> None:
        candidate, q1_only, q2_only = self._three_arms()
        record = q1_only["i04r1_response_record"]
        record["status"] = "invalid_window_protocol"
        record["B_after"] = None
        record["raw_response"] = None
        record["oriented_response"] = None
        record["operational_failure_id"] = "invalid-q1-window"
        q1_only["arrival_gain_receipt"]["expected_native_arrival_gain"] = None
        result = primary_margin(candidate, q1_only, q2_only, self.machine, self.parent)
        self.assertFalse(result["complete_three_arm_tuple_valid"])
        self.assertFalse(result["evaluable"])
        self.assertIsNone(result["selected_comparator_record_id"])
        self.assertIsNone(result["normalized_margin"])
        self.assertEqual(result["nonevaluable_record_ids"], ["q1-only"])

    def test_cross_order_or_pairing_max_is_rejected(self) -> None:
        candidate, q1_only, q2_only = self._three_arms()
        q2_only["i04r1_response_record"]["physical_order_id"] = "q2_then_q1"
        with self.assertRaises(ContractError):
            primary_margin(candidate, q1_only, q2_only, self.machine, self.parent)

    def test_arrival_gain_requires_identity_amount_domain_and_no_adjustment(self) -> None:
        candidate, _, _ = self._three_arms()
        validate_response_envelope(candidate, self.machine, self.parent)
        mismatched = deepcopy(candidate)
        mismatched["arrival_gain_receipt"]["expected_native_arrival_gain"] = 0.2
        with self.assertRaises(ContractError):
            validate_response_envelope(mismatched, self.machine, self.parent)
        outside = deepcopy(candidate)
        outside["arrival_gain_receipt"]["native_coherence_domain_upper"] = 0.1
        with self.assertRaises(ContractError):
            validate_response_envelope(outside, self.machine, self.parent)
        adjusted = deepcopy(candidate)
        adjusted["arrival_gain_receipt"]["arrival_adjustment_event_ids"] = ["clip-event"]
        with self.assertRaises(ContractError):
            validate_response_envelope(adjusted, self.machine, self.parent)

    def test_scientific_zero_requires_valid_empty_two_step_window(self) -> None:
        candidate, _, _ = self._three_arms()
        record = candidate["i04r1_response_record"]
        record.update(
            {
                "status": "scientific_no_response",
                "B_after": 0.0,
                "raw_response": 0.0,
                "oriented_response": 0.0,
                "step_processed_event_kinds": ["event_queue_empty", "event_queue_empty"],
                "producer_reason": "synthetic_analysis_no_event",
                "response_packet_id": None,
                "departure_event_id": None,
                "arrival_event_id": None,
                "response_packet_amount": None,
                "B_targeting_event_ids": [],
                "native_chain_evidence_refs": [],
            }
        )
        candidate["window_validity_receipt"]["step_processed_event_ids"] = [None, None]
        candidate["arrival_gain_receipt"]["expected_native_arrival_gain"] = 0.0
        candidate["arrival_gain_receipt"]["arrival_transform_id"] = "no_arrival"
        validate_response_envelope(candidate, self.machine, self.parent)
        candidate["window_validity_receipt"]["window_contamination_event_ids"] = [
            "unrelated-event"
        ]
        with self.assertRaises(ContractError):
            validate_response_envelope(candidate, self.machine, self.parent)

    def test_observed_step_event_identity_mismatch_is_rejected(self) -> None:
        candidate, _, _ = self._three_arms()
        candidate["window_validity_receipt"]["step_processed_event_ids"] = [
            "unrelated-departure",
            "candidate-arrival",
        ]
        with self.assertRaises(ContractError):
            validate_response_envelope(candidate, self.machine, self.parent)


if __name__ == "__main__":
    unittest.main()
