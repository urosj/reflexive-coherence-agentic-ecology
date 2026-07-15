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
from p2_i2_analysis import (  # noqa: E402
    classify_margin_panel,
    evaluate_numeric_rule,
    normalized_paired_difference,
    paired_margin,
    validate_analysis_policy,
    validate_response_record,
)
from p2_i2_calibration import validate_calibration_policy  # noqa: E402


class P2I2AnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.analysis = json.loads(
            (EXPERIMENT / "configs/p2_i2_analysis_policy.json").read_text()
        )
        cls.calibration = json.loads(
            (EXPERIMENT / "configs/p2_i2_calibration_policy.json").read_text()
        )

    def _record(
        self,
        *,
        record_id: str,
        response: float | None,
        status: str = "observed_response",
        cell: str = "combined-orders",
        pairing_identity: str = "pairing-fixture-independent-test",
        order: str = "source_role_1_then_source_role_2",
    ) -> dict[str, object]:
        scientific = status in {"observed_response", "scientific_no_response"}
        return {
            "record_id": record_id,
            "mode": "state_carried",
            "seed": 101,
            "order_id": order,
            "cell_id": cell,
            "subconfiguration_id": "analysis-unit-test-only",
            "pairing_identity": pairing_identity,
            "opportunity_id": "analysis-unit-test-opportunity",
            "response_id": "native_B_target_coherence_gain",
            "unit": "native_coherence_amount",
            "status": status,
            "raw_response": response,
            "oriented_response": response,
            "window_start_event_id": "window-start" if scientific else None,
            "window_end_event_id": "window-end" if scientific else None,
            "producer_evaluation_count": 1 if scientific else 0,
            "response_packet_ids": ["native-packet"] if status == "observed_response" else [],
            "native_chain_complete": scientific,
            "operational_failure_id": None if scientific else "unit-test-operational-failure",
        }

    def test_policies_validate_without_executing_null(self) -> None:
        validate_analysis_policy(self.analysis)
        validate_calibration_policy(self.calibration, self.analysis)

    def test_observed_and_no_response_records_validate(self) -> None:
        validate_response_record(self._record(record_id="observed", response=7.25))
        validate_response_record(
            self._record(
                record_id="no-response",
                response=0.0,
                status="scientific_no_response",
            )
        )

    def test_operational_missingness_requires_null_response(self) -> None:
        record = self._record(
            record_id="missing",
            response=None,
            status="missing_infrastructure",
        )
        validate_response_record(record)
        record["raw_response"] = 0.0
        with self.assertRaises(ContractError):
            validate_response_record(record)

    def test_negative_response_is_rejected(self) -> None:
        with self.assertRaises(ContractError):
            validate_response_record(self._record(record_id="negative", response=-0.125))

    def test_paired_margin_retains_raw_values(self) -> None:
        candidate = self._record(record_id="candidate", response=7.25)
        comparator = self._record(
            record_id="comparator",
            response=3.125,
            cell="individual-contributions",
        )
        result = paired_margin(candidate, comparator, self.analysis)
        self.assertTrue(result["evaluable"])
        self.assertEqual(result["candidate_response"], 7.25)
        self.assertEqual(result["comparator_response"], 3.125)
        self.assertAlmostEqual(
            result["normalized_margin"],
            normalized_paired_difference(7.25, 3.125, 1e-12),
        )

    def test_pairing_identity_drift_is_rejected(self) -> None:
        candidate = self._record(record_id="candidate", response=7.25)
        comparator = self._record(
            record_id="comparator",
            response=3.125,
            pairing_identity="different-pairing",
        )
        with self.assertRaises(ContractError):
            paired_margin(candidate, comparator, self.analysis)

    def test_operational_pair_is_not_evaluable(self) -> None:
        candidate = self._record(record_id="candidate", response=7.25)
        comparator = self._record(
            record_id="comparator",
            response=None,
            status="censored_runtime",
        )
        result = paired_margin(candidate, comparator, self.analysis)
        self.assertFalse(result["evaluable"])
        self.assertIsNone(result["normalized_margin"])

    def test_relation_vocabulary_boundaries(self) -> None:
        delta = 0.05
        self.assertEqual(classify_margin_panel([0.2, 0.3], delta), "robust_aligned")
        self.assertEqual(classify_margin_panel([0.2, 0.01], delta), "narrow_aligned")
        self.assertEqual(classify_margin_panel([0.01, -0.01], delta), "resolution_limited")
        self.assertEqual(classify_margin_panel([0.2, -0.2], delta), "mixed_direction")
        self.assertEqual(classify_margin_panel([-0.2, -0.01], delta), "narrow_counter")
        self.assertEqual(classify_margin_panel([-0.2, -0.3], delta), "robust_counter")
        self.assertEqual(classify_margin_panel([0.2, None], delta), "resolution_unknown")

    def test_numeric_machine_rules(self) -> None:
        delta = 0.05
        self.assertEqual(evaluate_numeric_rule("invariant", [0.01, -0.01], delta), "pass")
        self.assertEqual(evaluate_numeric_rule("invariant", [0.01, 0.2], delta), "fail")
        self.assertEqual(evaluate_numeric_rule("different_unsigned", [0.2, -0.2], delta), "pass")
        self.assertEqual(evaluate_numeric_rule("different_unsigned", [0.2, 0.01], delta), "ambiguous")
        self.assertEqual(evaluate_numeric_rule("aligned_all", [0.2, 0.3], delta), "pass")
        self.assertEqual(evaluate_numeric_rule("aligned_all", [0.2, -0.2], delta), "fail")
        self.assertEqual(evaluate_numeric_rule("access_relation_retained", [0.2, 0.3, 0.01], delta), "pass")
        self.assertEqual(evaluate_numeric_rule("access_relation_retained", [0.2, 0.01, 0.02], delta), "ambiguous")

    def test_policy_drift_fails_closed(self) -> None:
        drifted = deepcopy(self.analysis)
        drifted["required_modes"] = ["state_carried"]
        with self.assertRaises(ContractError):
            validate_analysis_policy(drifted)


if __name__ == "__main__":
    unittest.main()
