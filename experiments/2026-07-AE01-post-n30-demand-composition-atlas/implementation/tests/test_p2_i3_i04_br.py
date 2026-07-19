"""Focused pure tests for the P2-I3 B-R I04 machine contract."""

from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator
import pytest


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
from p2_i3_i04_br_analysis import (  # noqa: E402
    build_synthetic_response_record,
    estimate_woe_triplet,
    validate_response_record,
)
from p2_i3_i04_br_validate import validate_policy  # noqa: E402


POLICY_PATH = EXPERIMENT / "configs/p2_i3_br_i04_machine_policy.json"
SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i04-br-machine-records.schema.json"
ANALYSIS_PATH = EXPERIMENT / "scripts/p2_i3_i04_br_analysis.py"
VALIDATOR_PATH = EXPERIMENT / "scripts/p2_i3_i04_br_validate.py"
RETAINED_VALIDATION_PATH = EXPERIMENT / "contracts/p2-i3/i04-br-calibration-preregistration-validation.json"
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
EPSILON = POLICY["calibration"]["epsilon_mu"]["value"]


def pairing() -> dict:
    return {
        "calibration_stratum": "pure-unit-test",
        "deterministic_replicate": 0,
        "configuration_or_variation_id": "unit",
        "route_role": "tested-route",
        "clean_parent_identity": "clean-parent",
        "causal_continuation_projection_identity": "causal-projection",
        "encounter_index": 0,
        "request_construction_id": "fixed-request",
        "request_timing_id": "next-native-event",
        "future_schedule_identity": "equal-future",
        "observation_boundary_id": "pre-next-event",
    }


def triplet(*, w: str, o: str, e: str, pair_id: str = "unit-pair") -> list[dict]:
    values = {"W": w, "O": o, "E": e}
    return [
        build_synthetic_response_record(
            record_id=f"{pair_id}:{arm}",
            pair_id=pair_id,
            arm_id=arm,
            margin=values[arm],
            seed_alias=19,
            case_id="PURE-UNIT",
            pairing=pairing(),
        )
        for arm in ("W", "O", "E")
    ]


def validate_against(definition: str, value: dict) -> None:
    wrapper = {
        "$schema": SCHEMA["$schema"],
        "$defs": SCHEMA["$defs"],
        "$ref": f"#/$defs/{definition}",
    }
    Draft202012Validator(wrapper).validate(value)


def test_policy_and_schema_validate_without_calibration_invocation() -> None:
    checks = validate_policy(POLICY, SCHEMA)
    assert len(checks) >= 100
    assert POLICY["candidate_blind_boundary"]["i04_calibration_invocations"] == 0
    assert POLICY["future_i05_boundary"]["authorization_present"] is False


def test_schema_root_is_a_closed_record_union() -> None:
    validator = Draft202012Validator(SCHEMA)
    for invalid in ({}, {"nonsense": 1}, {"record_type": "garbage"}):
        assert not validator.is_valid(invalid)

    responses = triplet(w="0", o="1/4", e="1/4")
    result = estimate_woe_triplet(responses, epsilon_mu=EPSILON)
    assert validator.is_valid(responses[0])
    assert validator.is_valid(result["trace_relation"])
    assert validator.is_valid(result)


def test_pair_schema_closes_evaluable_and_nonevaluable_states() -> None:
    validator = Draft202012Validator(SCHEMA)
    pair = estimate_woe_triplet(triplet(w="0", o="1/4", e="1/4"), epsilon_mu=EPSILON)["trace_relation"]
    duplicate = deepcopy(pair)
    duplicate["arm_record_ids"] = [duplicate["arm_record_ids"][0]] * 2
    assert not validator.is_valid(duplicate)
    contradictory = deepcopy(pair)
    contradictory["nonevaluable_record_ids"] = [pair["arm_record_ids"][0]]
    assert not validator.is_valid(contradictory)
    contradictory = deepcopy(pair)
    contradictory["evaluable"] = False
    assert not validator.is_valid(contradictory)


def test_response_schema_closes_validity_and_source_class_states() -> None:
    validator = Draft202012Validator(SCHEMA)
    record = triplet(w="0", o="0", e="0")[0]
    contradictory = deepcopy(record)
    contradictory["admissibility_margin"] = None
    assert not validator.is_valid(contradictory)

    invalid = deepcopy(record)
    invalid["validity_status"] = "invalid_or_infrastructure_failure"
    invalid["native_disposition"] = "invalid_or_infrastructure_failure"
    invalid["admissibility_margin"] = None
    assert validator.is_valid(invalid)

    synthetic_drift = deepcopy(record)
    synthetic_drift["candidate_artifacts_consumed"] = True
    assert not validator.is_valid(synthetic_drift)

    live = deepcopy(record)
    live["source_class"] = "registered_live_response"
    live["calibration_seed_alias"] = None
    live["candidate_artifacts_consumed"] = True
    live["pygrc_runtime_inputs_consumed"] = True
    live["candidate_execution_performed"] = True
    validate_response_record(live)
    assert validator.is_valid(live)
    live["pygrc_runtime_inputs_consumed"] = False
    assert not validator.is_valid(live)
    with pytest.raises(ContractError):
        validate_response_record(live)


def test_raw_additive_identity_is_closed_and_required_when_evaluable() -> None:
    validator = Draft202012Validator(SCHEMA)
    result = estimate_woe_triplet(triplet(w="0", o="1/4", e="1/4"), epsilon_mu=EPSILON)
    extra = deepcopy(result)
    extra["raw_additive_identity"]["unregistered"] = 1
    assert not validator.is_valid(extra)
    false_identity = deepcopy(result)
    false_identity["raw_additive_identity"]["additive_identity_holds"] = False
    assert not validator.is_valid(false_identity)
    missing = deepcopy(result)
    missing["raw_additive_identity"] = None
    assert not validator.is_valid(missing)


def test_reconstruction_refuses_retained_validation_output() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--output", str(RETAINED_VALIDATION_PATH)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "refusing to overwrite retained validation" in completed.stderr


def test_analysis_module_has_no_pygrc_or_calibration_builder() -> None:
    source = ANALYSIS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in imports)
    assert "build_calibration_record" not in source


@pytest.mark.parametrize(
    ("margin", "disposition"),
    [
        ("-1/2", "field_limited_refusal"),
        ("0", "admitted"),
        ("1/2", "admitted"),
    ],
)
def test_typed_response_uses_strict_native_sign_boundary(
    margin: str, disposition: str
) -> None:
    record = triplet(w=margin, o=margin, e=margin)[0]
    validate_response_record(record)
    validate_against("response_record", record)
    assert record["native_disposition"] == disposition
    assert record["admissibility_margin"]["value"] == float(record["c_pre_m_e"]["value"] - 1.0)


def test_sign_disposition_mismatch_is_invalid_not_scientific() -> None:
    record = triplet(w="-1/4", o="-1/4", e="-1/4")[0]
    record["native_disposition"] = "admitted"
    with pytest.raises(ContractError):
        validate_response_record(record)


def test_exact_equal_triplet_produces_canonical_positive_zero() -> None:
    result = estimate_woe_triplet(triplet(w="-1/4", o="-1/4", e="-1/4"), epsilon_mu=EPSILON)
    validate_against("triplet_result", result)
    assert result["trace_relation"]["normalized_margin"] == 0.0
    assert result["export_relation"]["normalized_margin"] == 0.0
    assert str(result["trace_relation"]["normalized_margin"]) == "0.0"


def test_trace_and_export_orientation_and_raw_additive_identity() -> None:
    result = estimate_woe_triplet(triplet(w="1/10", o="3/10", e="1/5"), epsilon_mu=EPSILON)
    assert result["trace_relation"]["raw_numerator"] == pytest.approx(0.1)
    assert result["export_relation"]["raw_numerator"] == pytest.approx(0.1)
    assert result["raw_additive_identity"]["delta_formed"] == pytest.approx(0.2)
    assert result["raw_additive_identity"]["additive_identity_holds"] is True
    assert result["normalized_relations_additive"] is False


def test_cross_zero_is_unclipped_magnitude_two() -> None:
    trace = estimate_woe_triplet(triplet(w="-1/10", o="1/10", e="1/10"), epsilon_mu=EPSILON)
    export = estimate_woe_triplet(triplet(w="-1/10", o="1/10", e="-1/10"), epsilon_mu=EPSILON)
    assert trace["trace_relation"]["normalized_margin"] == pytest.approx(2.0)
    assert export["export_relation"]["normalized_margin"] == pytest.approx(2.0)
    assert trace["normalized_relations_clipped"] is False


def test_floor_dominance_and_floor_equality() -> None:
    dominated = estimate_woe_triplet(
        triplet(w="0", o="1/2000000000000", e="1/2000000000000"),
        epsilon_mu=EPSILON,
    )
    equality = estimate_woe_triplet(
        triplet(w="0", o="1/1000000000000", e="1/1000000000000"),
        epsilon_mu=EPSILON,
    )
    assert dominated["trace_relation"]["denominator_source"] == "epsilon_mu"
    assert dominated["trace_relation"]["normalized_margin"] == pytest.approx(0.5)
    assert equality["trace_relation"]["normalized_margin"] == pytest.approx(1.0)


def test_all_non_delta_estimator_conformance_cases_follow_frozen_assertions() -> None:
    for case in POLICY["calibration"]["panels_b_c_estimator_conformance"]:
        result = estimate_woe_triplet(
            triplet(
                w=case["values"]["W"],
                o=case["values"]["O"],
                e=case["values"]["E"],
                pair_id=case["case_id"],
            ),
            epsilon_mu=EPSILON,
        )
        trace = result["trace_relation"]
        export = result["export_relation"]
        assert trace["raw_numerator"] == float(
            Fraction(case["values"]["E"]) - Fraction(case["values"]["W"])
        )
        assert export["raw_numerator"] == float(
            Fraction(case["values"]["O"]) - Fraction(case["values"]["E"])
        )
        assert result["raw_additive_identity"]["additive_identity_holds"] is True
        validate_against("triplet_result", result)
        checks = {
            "m_trace_positive": trace["normalized_margin"] > 0,
            "m_trace_negative": trace["normalized_margin"] < 0,
            "m_trace_positive_zero": trace["normalized_margin"] == 0.0,
            "m_trace_equals_one_half": trace["normalized_margin"] == pytest.approx(0.5),
            "m_trace_equals_one": trace["normalized_margin"] == pytest.approx(1.0),
            "m_trace_equals_two": trace["normalized_margin"] == pytest.approx(2.0),
            "m_export_positive": export["normalized_margin"] > 0,
            "m_export_negative": export["normalized_margin"] < 0,
            "m_export_positive_zero": export["normalized_margin"] == 0.0,
            "m_export_equals_two": export["normalized_margin"] == pytest.approx(2.0),
            "trace_denominator_first_arm": trace["denominator_source"] == "first_arm",
            "trace_denominator_second_arm": trace["denominator_source"] == "second_arm",
            "trace_denominator_epsilon_mu": trace["denominator_source"] == "epsilon_mu",
            "export_denominator_first_arm": export["denominator_source"] == "first_arm",
            "export_denominator_second_arm": export["denominator_source"] == "second_arm",
            "unclipped": result["normalized_relations_clipped"] is False,
            "non_dyadic_round_trip": True,
        }
        for assertion in case["assertions"]:
            assert checks[assertion], f"{case['case_id']} failed {assertion}"


def test_invalid_w_arm_blocks_trace_pair_but_not_unrelated_export_pair() -> None:
    records = triplet(w="0", o="1/4", e="1/4")
    invalid_w = records[0]
    invalid_w["validity_status"] = "invalid_or_infrastructure_failure"
    invalid_w["native_disposition"] = "invalid_or_infrastructure_failure"
    invalid_w["admissibility_margin"] = None
    result = estimate_woe_triplet(records, epsilon_mu=EPSILON)
    assert result["trace_relation"]["evaluable"] is False
    assert result["trace_relation"]["normalized_margin"] is None
    assert result["export_relation"]["evaluable"] is True
    assert result["raw_additive_identity"] is None


def test_invalid_e_arm_blocks_both_pairs_without_surviving_arm_substitution() -> None:
    records = triplet(w="0", o="1/4", e="1/4")
    invalid_e = records[2]
    invalid_e["validity_status"] = "invalid_or_infrastructure_failure"
    invalid_e["native_disposition"] = "invalid_or_infrastructure_failure"
    invalid_e["admissibility_margin"] = None
    result = estimate_woe_triplet(records, epsilon_mu=EPSILON)
    assert result["trace_relation"]["evaluable"] is False
    assert result["export_relation"]["evaluable"] is False


def test_pairing_mismatch_fails_closed() -> None:
    records = triplet(w="0", o="1/4", e="1/4")
    records[2]["pairing"] = deepcopy(records[2]["pairing"])
    records[2]["pairing"]["future_schedule_identity"] = "different-future"
    with pytest.raises(ContractError):
        estimate_woe_triplet(records, epsilon_mu=EPSILON)


def test_schema_rejects_extra_response_field() -> None:
    record = triplet(w="0", o="0", e="0")[0]
    record["candidate_value"] = 1.0
    with pytest.raises(Exception):
        validate_against("response_record", record)


def test_control_schema_keeps_lifecycle_fields_orthogonal() -> None:
    row = POLICY["control_governance"]["common_control_legs"][0]
    state = {
        "leg_id": row["leg_id"],
        "parent_control_id": row["parent_control_id"],
        "applicability": row["applicability"],
        "control_class": row["control_class"],
        "evidence_types": row["evidence_types"],
        "execution_status": "not_due",
        "evidence_resolution": "not_evaluated",
        "control_resolution": "unresolved",
        "terminal_guard_status": "not_armed",
    }
    validate_against("control_leg_state", state)
    broken = deepcopy(state)
    broken["execution_status"] = "pass"
    with pytest.raises(Exception):
        validate_against("control_leg_state", broken)


def test_terminal_overlay_cannot_claim_it_changed_i09_facts() -> None:
    overlay = {
        "overlay_id": "overlay",
        "control_index_identity": "i09",
        "reconstruction_identity": "i10",
        "terminal_class_valid": True,
        "claim_vocabulary_valid": True,
        "selection_record_valid": True,
        "demand_native_separation_valid": True,
        "report_language_valid": True,
        "i09_scientific_facts_changed": False,
    }
    validate_against("terminal_guard_overlay", overlay)
    overlay["i09_scientific_facts_changed"] = True
    with pytest.raises(Exception):
        validate_against("terminal_guard_overlay", overlay)
