"""Pure builder for the governed P2-I3 B-R arithmetic calibration.

Importing this module performs no calibration, file write, PyGRC import, or
candidate operation.  The complete builder may be called only by the accepted
I05 one-shot wrapper after its permanent attempt claim is created.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Any, Mapping

from ae01_tooling import ContractError
from p2_i3_i04_br_analysis import (
    build_synthetic_response_record,
    estimate_woe_triplet,
    parse_rational,
    rational_string,
    validate_response_record,
)


POLICY_ID = "P2-I3-I05-BR-ONE-SHOT-POLICY"
FREEZE_ID = "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE"
I04_POLICY_ID = "rcae-p2-i3-br-i04-machine-policy-v1"
I04_SOURCE_ANCHOR = "1097547ad30b77d4cf9312fb05753902f6d1cc81"
REQUEST_CONSTRUCTION_ID = "p2-i3-i05-q-half-v1"
Q_PROBE = Fraction(1, 2)
ARTIFACT_VERSION = "1.0.2"
CALIBRATED_RELATION_IDS = ["m_trace", "m_export"]
RELATION_KEYS = {"m_trace": "trace_relation", "m_export": "export_relation"}
ENTERED_CASES = [
    ("EQ-NEG-HALF", 19, "-1/2"),
    ("EQ-NEG-QUARTER", 43, "-1/4"),
    ("EQ-ZERO", 71, "0"),
    ("EQ-POS-QUARTER", 109, "1/4"),
    ("EQ-POS-HALF", 163, "1/2"),
]
EXCLUDED_CONFORMANCE_CASE_IDS = [
    "TRACE-FIRST-DOM-POS",
    "TRACE-SECOND-DOM-NEG",
    "EXPORT-FIRST-DOM-POS",
    "EXPORT-SECOND-DOM-NEG",
    "FLOOR-DOM-POS",
    "FLOOR-EQUALITY",
    "TRACE-CROSS-ZERO",
    "EXPORT-CROSS-ZERO",
]
MATCHED_NULL_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "outputs/p2-i3/i05/br-matched-null.json"
)
DELTA_FORMULA = (
    "max(measurement_resolution, max(abs(m_trace[c]), abs(m_export[c])) "
    "for c in entered_case_ids)"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _rational_value(value: Fraction) -> dict[str, Any]:
    return {"rational": rational_string(value), "value": float(value)}


def _validate_rational_value(value: Mapping[str, Any], label: str) -> Fraction:
    _require(set(value) == {"rational", "value"}, f"{label} shape drifted")
    rational = parse_rational(value["rational"])
    _require(rational_string(rational) == value["rational"], f"{label} is not canonical")
    projected = value["value"]
    _require(isinstance(projected, (int, float)) and not isinstance(projected, bool), f"{label} value is not numeric")
    _require(math.isfinite(float(projected)), f"{label} value is not finite")
    _require(float(projected) == float(rational), f"{label} rational/value mismatch")
    if rational == 0:
        _require(value["rational"] == "0", f"{label} zero is not canonical")
        _require(math.copysign(1.0, float(projected)) == 1.0, f"{label} uses negative zero")
    return rational


def _authority() -> dict[str, str]:
    return {
        "freeze_id": FREEZE_ID,
        "i04_source_anchor": I04_SOURCE_ANCHOR,
        "policy_id": POLICY_ID,
    }


def _exact_normalized_margin(
    first: Mapping[str, Any], second: Mapping[str, Any], epsilon: Fraction
) -> Fraction:
    """Compute the registered normalized margin without a float round trip."""

    first_mu = _validate_rational_value(first["admissibility_margin"], "first margin")
    second_mu = _validate_rational_value(second["admissibility_margin"], "second margin")
    denominator = max(abs(first_mu), abs(second_mu), epsilon)
    _require(denominator > 0, "exact normalized denominator must be positive")
    return (first_mu - second_mu) / denominator


def exact_triplet_margins(
    records: list[Mapping[str, Any]], epsilon: Fraction
) -> tuple[Fraction, Fraction]:
    """Return exact trace/export margins from one unique W/O/E record set."""

    _require(len(records) == 3, "exactly three responses are required")
    by_arm = {str(record.get("arm_id")): record for record in records}
    _require(set(by_arm) == {"W", "O", "E"} and len(by_arm) == 3, "one unique W/O/E response is required")
    return (
        _exact_normalized_margin(by_arm["E"], by_arm["W"], epsilon),
        _exact_normalized_margin(by_arm["O"], by_arm["E"], epsilon),
    )


def _pairing(case_id: str, seed_alias: int) -> dict[str, Any]:
    return {
        "calibration_stratum": "panel-a-exact-null",
        "deterministic_replicate": seed_alias,
        "configuration_or_variation_id": case_id,
        "route_role": "arithmetic-null-no-route",
        "clean_parent_identity": "candidate-blind-arithmetic-parent-v1",
        "causal_continuation_projection_identity": "not-applicable-arithmetic-null",
        "encounter_index": 0,
        "request_construction_id": REQUEST_CONSTRUCTION_ID,
        "request_timing_id": "synthetic-pre-next-event",
        "future_schedule_identity": "not-applicable-arithmetic-null",
        "observation_boundary_id": "synthetic-exact-response",
    }


def build_q_half_response(
    *, case_id: str, arm_id: str, margin: str, seed_alias: int
) -> dict[str, Any]:
    """Build one I05 arithmetic response with the accepted half-unit request.

    I04 owns the response envelope and validator.  I05 owns only the formerly
    deferred arithmetic construction, replacing the I04 test helper's local
    request fixture before revalidating the complete record.
    """

    mu = parse_rational(margin)
    c_pre = Q_PROBE + mu
    _require(Fraction(0) <= c_pre <= Fraction(1), "I05 carrier must remain in [0, 1]")
    pair_id = f"P2-I3-I05:{case_id}"
    record = build_synthetic_response_record(
        record_id=f"{pair_id}:{arm_id}",
        pair_id=pair_id,
        arm_id=arm_id,
        margin=margin,
        seed_alias=seed_alias,
        case_id=case_id,
        pairing=_pairing(case_id, seed_alias),
    )
    record["c_pre_m_e"] = _rational_value(c_pre)
    record["q_probe"] = _rational_value(Q_PROBE)
    validate_response_record(record)
    return record


def validate_builder_authorities(
    i04_policy: Mapping[str, Any], metric_sheet: Mapping[str, Any]
) -> None:
    _require(i04_policy.get("policy_id") == I04_POLICY_ID, "I04 policy drifted")
    panel = i04_policy.get("calibration", {}).get("panel_a_exact_null", [])
    _require(len(panel) == 5, "I04 exact-null panel must contain five cases")
    _require(
        i04_policy.get("future_i05_boundary", {})
        .get("canonical_arithmetic_response_construction", {})
        .get("candidate_shaped_arguments_allowed")
        is False,
        "I04 candidate-shaped-input boundary drifted",
    )
    record = metric_sheet.get("record", {})
    _require(record.get("lane_id") == "AE01-L03", "metric-sheet lane drifted")
    _require(
        record.get("metric_id") == "trace_conditioned_route_normalized_margin",
        "metric-sheet metric drifted",
    )
    _require(
        record.get("resolution_policy", {}).get("delta", {}).get("status") == "pending",
        "source metric sheet must remain pre-calibration",
    )
    panel_registry = [
        (case.get("case_id"), case.get("seed_alias"), case.get("values", {}).get("W"))
        for case in panel
    ]
    _require(panel_registry == ENTERED_CASES, "I04 exact-null case registry drifted")
    _require(
        all(set(case["values"]) == {"W", "O", "E"} and len(set(case["values"].values())) == 1 for case in panel),
        "I04 exact-null arms drifted",
    )
    excluded = [
        case.get("case_id")
        for case in i04_policy.get("calibration", {}).get("panels_b_c_estimator_conformance", [])
    ]
    _require(excluded == EXCLUDED_CONFORMANCE_CASE_IDS, "I04 excluded conformance registry drifted")


def validate_null_case(
    case: Mapping[str, Any], *, expected_id: str, expected_seed: int, expected_margin: str, epsilon: Fraction
) -> tuple[Fraction, Fraction]:
    """Semantically validate one retained null case without building the full panel."""

    _require(case.get("case_id") == expected_id, "null case identity drifted")
    _require(case.get("seed_alias") == expected_seed, "null case seed alias drifted")
    records = case.get("response_records")
    _require(isinstance(records, list) and len(records) == 3, "null case requires three responses")
    _require([record.get("arm_id") for record in records] == ["W", "O", "E"], "null case requires exact W/O/E arm order")
    pair_id = f"P2-I3-I05:{expected_id}"
    for record, arm in zip(records, ("W", "O", "E"), strict=True):
        validate_response_record(record)
        _require(record.get("record_id") == f"{pair_id}:{arm}", "response identity drifted")
        _require(record.get("pair_id") == pair_id, "response pair identity drifted")
        _require(record.get("case_id") == expected_id, "response case identity drifted")
        _require(record.get("calibration_seed_alias") == expected_seed, "response seed alias drifted")
        _require(record.get("pairing", {}).get("configuration_or_variation_id") == expected_id, "pairing case identity drifted")
        _require(record.get("pairing", {}).get("deterministic_replicate") == expected_seed, "pairing seed alias drifted")
        _require(_validate_rational_value(record["q_probe"], "q_probe") == Q_PROBE, "q_probe drifted")
        c_pre = _validate_rational_value(record["c_pre_m_e"], "c_pre_m_e")
        margin = _validate_rational_value(record["admissibility_margin"], "admissibility_margin")
        _require(margin == parse_rational(expected_margin), "registered margin drifted")
        _require(c_pre - Q_PROBE == margin, "half-unit arithmetic identity failed")
    recomputed = estimate_woe_triplet(records, epsilon_mu=float(epsilon))
    _require(case.get("triplet_result") == recomputed, "triplet result does not recompute exactly")
    _require(recomputed.get("pair_id") == pair_id, "triplet pair identity drifted")
    exact_margins = exact_triplet_margins(records, epsilon)
    for relation_id, exact_margin in zip(CALIBRATED_RELATION_IDS, exact_margins, strict=True):
        relation = recomputed[RELATION_KEYS[relation_id]]
        _require(relation.get("relation_id") == relation_id, "triplet relation identity drifted")
        _require(relation.get("pair_id") == pair_id and relation.get("evaluable") is True, "triplet relation is not evaluable")
        _require(float(exact_margin) == relation.get("normalized_margin"), "projected normalized margin drifted from exact value")
    return exact_margins


def validate_calibration_outputs(
    outputs: Mapping[str, Mapping[str, Any]],
    *,
    i04_policy: Mapping[str, Any],
    metric_sheet: Mapping[str, Any],
    source_metric_sheet_sha256: str,
) -> None:
    """Validate the complete output bundle, including cross-record semantics."""

    validate_builder_authorities(i04_policy, metric_sheet)
    _require(set(outputs) == {"matched_null", "metric_calibration", "frozen_metric_sheet"}, "output bundle shape drifted")
    matched = outputs["matched_null"]
    calibration = outputs["metric_calibration"]
    sheet = outputs["frozen_metric_sheet"]
    exact_authority = _authority()
    for artifact in outputs.values():
        _require(artifact.get("artifact_version") == ARTIFACT_VERSION, "output artifact version drifted")
        _require(artifact.get("authority") == exact_authority, "output authority drifted")
    cases = matched.get("cases")
    _require(isinstance(cases, list) and len(cases) == len(ENTERED_CASES), "matched-null case count drifted")
    epsilon = parse_rational(i04_policy["calibration"]["epsilon_mu"]["rational"])
    margins: list[Fraction] = []
    for case, (case_id, seed, margin) in zip(cases, ENTERED_CASES, strict=True):
        margins.extend(validate_null_case(case, expected_id=case_id, expected_seed=seed, expected_margin=margin, epsilon=epsilon))
    _require(len(margins) == 10, "shared calibration must contain ten margins")
    maximum = max(abs(value) for value in margins)
    delta = max(epsilon, maximum)
    _require(calibration.get("calibrated_relation_ids") == CALIBRATED_RELATION_IDS, "calibrated relation coverage drifted")
    _require(calibration.get("entered_case_ids") == [item[0] for item in ENTERED_CASES], "entered case registry drifted")
    _require(calibration.get("entered_margin_count") == 10, "entered margin count drifted")
    _require(calibration.get("margins_per_case") == {"m_trace": 1, "m_export": 1}, "per-case relation coverage drifted")
    _require(calibration.get("excluded_conformance_case_ids") == EXCLUDED_CONFORMANCE_CASE_IDS, "excluded case registry drifted")
    _require(calibration.get("matched_null_artifact_path") == MATCHED_NULL_PATH, "matched-null path drifted")
    _require(calibration.get("delta_formula") == DELTA_FORMULA, "delta formula drifted")
    expected_margin_rows = [
        {
            "case_id": case_id,
            "m_export": _rational_value(margins[index * 2 + 1]),
            "m_trace": _rational_value(margins[index * 2]),
        }
        for index, (case_id, _, _) in enumerate(ENTERED_CASES)
    ]
    _require(calibration.get("entered_margins") == expected_margin_rows, "exact entered-margin ledger drifted")
    _require(_validate_rational_value(calibration["maximum_absolute_matched_null_margin"], "maximum null margin") == maximum, "maximum null margin does not recompute")
    _require(_validate_rational_value(calibration["measurement_resolution"], "measurement resolution") == epsilon, "measurement resolution drifted")
    _require(_validate_rational_value(calibration["delta"], "delta") == delta, "delta does not recompute")
    _require(sheet.get("calibrated_relation_ids") == CALIBRATED_RELATION_IDS, "metric sheet relation coverage drifted")
    _require(sheet.get("delta_scope") == "shared_arithmetic_resolution_for_both_relations", "metric sheet delta scope drifted")
    _require(sheet.get("source_metric_sheet_sha256") == source_metric_sheet_sha256, "source metric sheet digest drifted")
    _require(_validate_rational_value(sheet["measurement_resolution"], "sheet measurement resolution") == epsilon, "sheet measurement resolution drifted")
    _require(_validate_rational_value(sheet["delta"], "sheet delta") == delta, "sheet delta drifted")


def build_calibration_outputs(
    *,
    i04_policy: Mapping[str, Any],
    metric_sheet: Mapping[str, Any],
    source_metric_sheet_sha256: str,
) -> dict[str, dict[str, Any]]:
    """Build all three deterministic outputs for one governed invocation."""

    validate_builder_authorities(i04_policy, metric_sheet)
    epsilon = parse_rational(i04_policy["calibration"]["epsilon_mu"]["rational"])
    null_cases: list[dict[str, Any]] = []
    normalized_margins: list[Fraction] = []
    for case in i04_policy["calibration"]["panel_a_exact_null"]:
        records = [
            build_q_half_response(
                case_id=case["case_id"],
                arm_id=arm,
                margin=case["values"][arm],
                seed_alias=case["seed_alias"],
            )
            for arm in ("W", "O", "E")
        ]
        triplet = estimate_woe_triplet(records, epsilon_mu=float(epsilon))
        _require(triplet["trace_relation"]["evaluable"], "trace null must be evaluable")
        _require(triplet["export_relation"]["evaluable"], "export null must be evaluable")
        exact_margins = exact_triplet_margins(records, epsilon)
        for key, exact_margin in zip(("trace_relation", "export_relation"), exact_margins, strict=True):
            _require(
                triplet[key]["normalized_margin"] == float(exact_margin),
                "I04 projection drifted from I05 exact arithmetic",
            )
        normalized_margins.extend(exact_margins)
        null_cases.append(
            {
                "case_id": case["case_id"],
                "response_records": records,
                "seed_alias": case["seed_alias"],
                "triplet_result": triplet,
            }
        )

    maximum = max(abs(value) for value in normalized_margins)
    delta = max(epsilon, maximum)
    matched_null = {
        "artifact_id": "P2-I3-I05-BR-MATCHED-NULL",
        "artifact_version": ARTIFACT_VERSION,
        "authority": _authority(),
        "candidate_artifacts_consumed": False,
        "candidate_execution_performed": False,
        "case_count": len(null_cases),
        "cases": null_cases,
        "evidence_effect": "numeric_measurement_resolution_only",
        "lane_id": "AE01-L03",
        "pygrc_runtime_inputs_consumed": False,
        "randomness_used": False,
        "response_record_count": sum(len(case["response_records"]) for case in null_cases),
        "scientific_result": False,
    }
    metric_calibration = {
        "artifact_id": "P2-I3-I05-BR-METRIC-CALIBRATION",
        "artifact_version": ARTIFACT_VERSION,
        "authority": _authority(),
        "candidate_blind": True,
        "delta": _rational_value(delta),
        "calibrated_relation_ids": CALIBRATED_RELATION_IDS,
        "delta_formula": DELTA_FORMULA,
        "entered_case_ids": [case["case_id"] for case in null_cases],
        "entered_margin_count": len(normalized_margins),
        "entered_margins": [
            {
                "case_id": case["case_id"],
                "m_export": _rational_value(normalized_margins[index * 2 + 1]),
                "m_trace": _rational_value(normalized_margins[index * 2]),
            }
            for index, case in enumerate(null_cases)
        ],
        "excluded_conformance_case_ids": EXCLUDED_CONFORMANCE_CASE_IDS,
        "lane_id": "AE01-L03",
        "margins_per_case": {"m_trace": 1, "m_export": 1},
        "matched_null_artifact_path": MATCHED_NULL_PATH,
        "maximum_absolute_matched_null_margin": _rational_value(maximum),
        "measurement_resolution": _rational_value(epsilon),
        "scientific_result": False,
    }
    source_record = metric_sheet["record"]
    frozen_metric_sheet = {
        "artifact_id": "P2-I3-I05-BR-FROZEN-METRIC-SHEET",
        "artifact_version": ARTIFACT_VERSION,
        "authority": _authority(),
        "candidate_blind": True,
        "calibrated_relation_ids": CALIBRATED_RELATION_IDS,
        "delta": _rational_value(delta),
        "delta_scope": "shared_arithmetic_resolution_for_both_relations",
        "evidence_effect": "numeric_measurement_resolution_only",
        "lane_id": "AE01-L03",
        "measurement_resolution": _rational_value(epsilon),
        "metric_id": source_record["metric_id"],
        "metric_sheet_id": source_record["metric_sheet_id"],
        "source_metric_sheet_sha256": source_metric_sheet_sha256,
        "status": "frozen_candidate_blind_calibration",
    }
    outputs = {
        "matched_null": matched_null,
        "metric_calibration": metric_calibration,
        "frozen_metric_sheet": frozen_metric_sheet,
    }
    validate_calibration_outputs(
        outputs,
        i04_policy=i04_policy,
        metric_sheet=metric_sheet,
        source_metric_sheet_sha256=source_metric_sheet_sha256,
    )
    return outputs
