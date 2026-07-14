"""Pure deterministic measurement analysis for P2-I2.

This module has no PyGRC dependency and performs no file I/O. The I05 matched
null and later registered live records must use the same response validation,
pairing, margin, and relation-classification functions defined here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import math
from typing import Any

from ae01_tooling import ContractError


MODES = ("state_carried", "history_carried", "hybrid")
ORDERS = (
    "source_role_1_then_source_role_2",
    "source_role_2_then_source_role_1",
)
SCIENTIFIC_STATUSES = ("observed_response", "scientific_no_response")
OPERATIONAL_STATUSES = (
    "censored_runtime",
    "missing_infrastructure",
    "blocked_by_control",
)
RELATIONS = (
    "robust_aligned",
    "narrow_aligned",
    "resolution_limited",
    "mixed_direction",
    "narrow_counter",
    "robust_counter",
    "resolution_unknown",
    "not_applicable",
)


def _finite_number(value: Any, *, context: str) -> float:
    if isinstance(value, bool):
        raise ContractError(f"{context} must be numeric, not boolean")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{context} must be numeric") from exc
    if not math.isfinite(number):
        raise ContractError(f"{context} must be finite")
    return number


def validate_analysis_policy(policy: Mapping[str, Any]) -> None:
    """Fail closed when the I04 scientific measurement policy drifts."""

    if policy.get("policy_id") != "rcae-p2-i2-three-mode-analysis-policy-v1":
        raise ContractError("P2-I2 analysis policy identity drifted")
    if tuple(policy.get("required_modes", ())) != MODES:
        raise ContractError("P2-I2 must retain all three modes in order")
    measurement = policy.get("measurement")
    if not isinstance(measurement, Mapping):
        raise ContractError("measurement policy must be an object")
    if measurement.get("response_id") != "native_B_target_coherence_gain":
        raise ContractError("primary later-continuation response drifted")
    if measurement.get("unit") != "native_coherence_amount":
        raise ContractError("raw response unit drifted")
    if measurement.get("orientation_transform") != "identity":
        raise ContractError("P2-I2 orientation must remain identity")
    window = measurement.get("window")
    if not isinstance(window, Mapping):
        raise ContractError("response window must be an object")
    if window.get("producer_evaluations") != 1:
        raise ContractError("response window requires exactly one producer evaluation")
    if window.get("registered_later_opportunities_per_cell_seed_subconfiguration_order") != 1:
        raise ContractError("response aggregation requires exactly one registered opportunity")

    equivalence = policy.get("cross_mode_semantic_equivalence")
    if not isinstance(equivalence, Mapping):
        raise ContractError("cross-mode equivalence proof missing")
    if any(
        equivalence.get(field) is not True
        for field in (
            "shared_response_definition",
            "shared_analysis_identity",
            "shared_calibration_identity",
        )
    ):
        raise ContractError("shared analysis surfaces require an affirmative proof")
    required_proof = {
        "causal_response_meaning",
        "unit_and_orientation",
        "time_window",
        "comparator_role",
        "aggregation",
        "missingness",
        "calibration_population",
    }
    proof = equivalence.get("proof")
    if not isinstance(proof, Mapping) or set(proof) != required_proof:
        raise ContractError("cross-mode semantic-equivalence fields drifted")

    pairing = policy.get("primary_pairing")
    if not isinstance(pairing, Mapping):
        raise ContractError("primary pairing must be an object")
    if pairing.get("candidate_cell") != "combined-orders":
        raise ContractError("primary candidate cell drifted")
    if pairing.get("comparator_cell") != "individual-contributions":
        raise ContractError("primary comparator cell drifted")
    if pairing.get("comparator_subconfiguration") != "quantity_and_timing_matched_single_source_repetition":
        raise ContractError("closest insufficient-repetition comparator drifted")
    order_rows = pairing.get("order_strata")
    if not isinstance(order_rows, list) or [row.get("order_id") for row in order_rows] != list(ORDERS):
        raise ContractError("both primary order strata must remain frozen")
    if "scalar-collapse" not in str(pairing.get("order_policy")):
        raise ContractError("order scalar-collapse prohibition missing")

    aggregation = policy.get("aggregation_and_missingness")
    if not isinstance(aggregation, Mapping):
        raise ContractError("aggregation and missingness policy missing")
    if aggregation.get("candidate_seeds") != [101, 211, 307]:
        raise ContractError("candidate seed policy drifted")
    if aggregation.get("opportunity_count_per_registered_stratum") != 1:
        raise ContractError("fixed opportunity denominator drifted")
    if tuple(aggregation.get("scientific_statuses", ())) != SCIENTIFIC_STATUSES:
        raise ContractError("scientific status vocabulary drifted")
    if tuple(aggregation.get("operational_statuses", ())) != OPERATIONAL_STATUSES:
        raise ContractError("operational status vocabulary drifted")

    margin = policy.get("paired_margin")
    if not isinstance(margin, Mapping):
        raise ContractError("paired margin policy missing")
    resolution = _finite_number(
        margin.get("measurement_resolution"), context="measurement resolution"
    )
    if resolution != 1e-12:
        raise ContractError("measurement resolution must remain the L02 sheet value")
    if margin.get("retain_per_seed_margins") is not True:
        raise ContractError("per-seed margins must be retained")

    classifier = policy.get("relation_classifier")
    if not isinstance(classifier, Mapping):
        raise ContractError("relation classifier missing")
    if "both order strata" not in str(classifier.get("top_primary_signature")):
        raise ContractError("top primary signature must require both orders")
    rules = policy.get("machine_rule_vocabulary")
    if not isinstance(rules, Mapping):
        raise ContractError("machine rule vocabulary missing")
    if set(rules) != {
        "invariant",
        "different_unsigned",
        "aligned_all",
        "raw_visibility",
        "causal_chain_exclusion",
        "access_relation_retained",
    }:
        raise ContractError("machine rule vocabulary drifted")
    for rule_name, rule in rules.items():
        if not isinstance(rule, Mapping) or set(rule) != {"pass", "ambiguous", "fail"}:
            raise ContractError(f"machine rule {rule_name} is incomplete")

    common_rules = policy.get("common_control_rules")
    mode_rules = policy.get("mode_control_rules")
    if not isinstance(common_rules, list) or len(common_rules) != 9:
        raise ContractError("nine common control/diagnostic rules are required")
    if not isinstance(mode_rules, Mapping) or tuple(mode_rules) != MODES:
        raise ContractError("mode control rules must retain all modes in order")
    if [len(mode_rules[mode]) for mode in MODES] != [3, 3, 5]:
        raise ContractError("mode control rule counts drifted")
    if not any(
        row.get("control_id") == "complete_P_by_H_P_component_factorial"
        for row in mode_rules["hybrid"]
    ):
        raise ContractError("complete hybrid component factorial missing")

    terminal = policy.get("terminal_input_boundary")
    if not isinstance(terminal, Mapping):
        raise ContractError("terminal input boundary missing")
    if terminal.get("terminal_classification_deferred") is not True:
        raise ContractError("terminal classification must remain deferred")
    if terminal.get("mode_selection_or_ranking_forbidden") is not True:
        raise ContractError("mode selection or ranking must remain forbidden")


_RESPONSE_FIELDS = {
    "record_id",
    "mode",
    "seed",
    "order_id",
    "cell_id",
    "subconfiguration_id",
    "pairing_identity",
    "opportunity_id",
    "response_id",
    "unit",
    "status",
    "raw_response",
    "oriented_response",
    "window_start_event_id",
    "window_end_event_id",
    "producer_evaluation_count",
    "response_packet_ids",
    "native_chain_complete",
    "operational_failure_id",
}


def validate_response_record(record: Mapping[str, Any]) -> None:
    """Validate one later-continuation response at the analysis boundary."""

    if set(record) != _RESPONSE_FIELDS:
        missing = sorted(_RESPONSE_FIELDS - set(record))
        unknown = sorted(set(record) - _RESPONSE_FIELDS)
        raise ContractError(
            f"response record fields drifted; missing={missing}, unknown={unknown}"
        )
    if record["mode"] not in MODES:
        raise ContractError("response record mode is not retained")
    if record["order_id"] not in (*ORDERS, "not_ordered"):
        raise ContractError("response record order identity is invalid")
    if record["response_id"] != "native_B_target_coherence_gain":
        raise ContractError("response record field identity drifted")
    if record["unit"] != "native_coherence_amount":
        raise ContractError("response record unit drifted")
    if not isinstance(record["seed"], int) or isinstance(record["seed"], bool):
        raise ContractError("response seed must be an integer")
    for field in (
        "record_id",
        "cell_id",
        "subconfiguration_id",
        "pairing_identity",
        "opportunity_id",
    ):
        if not isinstance(record[field], str) or not record[field]:
            raise ContractError(f"{field} must be a non-empty string")
    packet_ids = record["response_packet_ids"]
    if not isinstance(packet_ids, list) or any(
        not isinstance(item, str) or not item for item in packet_ids
    ):
        raise ContractError("response packet IDs must be a string list")

    status = record["status"]
    if status in SCIENTIFIC_STATUSES:
        raw = _finite_number(record["raw_response"], context="raw response")
        oriented = _finite_number(
            record["oriented_response"], context="oriented response"
        )
        if raw < 0.0 or oriented != raw:
            raise ContractError("scientific response must be finite, nonnegative, and identity-oriented")
        if record["producer_evaluation_count"] != 1:
            raise ContractError("scientific response requires one producer evaluation")
        if record["native_chain_complete"] is not True:
            raise ContractError("scientific response requires a complete native chain")
        if record["operational_failure_id"] is not None:
            raise ContractError("scientific response cannot carry an operational failure")
        if not all(
            isinstance(record[field], str) and record[field]
            for field in ("window_start_event_id", "window_end_event_id")
        ):
            raise ContractError("scientific response window IDs must be present")
        if status == "scientific_no_response":
            if raw != 0.0 or packet_ids:
                raise ContractError("scientific no-response requires zero and no response packet")
        elif raw <= 0.0 or len(packet_ids) != 1:
            raise ContractError("observed response requires positive B gain and one packet")
    elif status in OPERATIONAL_STATUSES:
        if record["raw_response"] is not None or record["oriented_response"] is not None:
            raise ContractError("operationally incomplete response values must be null")
        if not isinstance(record["operational_failure_id"], str) or not record["operational_failure_id"]:
            raise ContractError("operationally incomplete response requires a failure ID")
    else:
        raise ContractError("unknown response status")


def normalized_paired_difference(
    candidate: float,
    comparator: float,
    measurement_resolution: float,
) -> float:
    """Return the frozen oriented paired normalized difference."""

    left = _finite_number(candidate, context="candidate response")
    right = _finite_number(comparator, context="comparator response")
    floor = _finite_number(measurement_resolution, context="measurement resolution")
    if left < 0.0 or right < 0.0 or floor <= 0.0:
        raise ContractError("paired responses must be nonnegative and resolution positive")
    return (left - right) / max(abs(left), abs(right), floor)


def paired_margin(
    candidate: Mapping[str, Any],
    comparator: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Pair two registered response records without hiding raw coverage."""

    validate_analysis_policy(policy)
    validate_response_record(candidate)
    validate_response_record(comparator)
    pairing_fields = ("mode", "seed", "order_id", "pairing_identity")
    drift = [field for field in pairing_fields if candidate[field] != comparator[field]]
    if drift:
        raise ContractError(f"paired response identity drifted: {drift}")
    candidate_scientific = candidate["status"] in SCIENTIFIC_STATUSES
    comparator_scientific = comparator["status"] in SCIENTIFIC_STATUSES
    evaluable = candidate_scientific and comparator_scientific
    margin = None
    if evaluable:
        margin = normalized_paired_difference(
            float(candidate["oriented_response"]),
            float(comparator["oriented_response"]),
            float(policy["paired_margin"]["measurement_resolution"]),
        )
    return {
        "mode": candidate["mode"],
        "seed": candidate["seed"],
        "order_id": candidate["order_id"],
        "pairing_identity": candidate["pairing_identity"],
        "candidate_record_id": candidate["record_id"],
        "comparator_record_id": comparator["record_id"],
        "candidate_response": candidate["oriented_response"],
        "comparator_response": comparator["oriented_response"],
        "evaluable": evaluable,
        "normalized_margin": margin,
    }


def classify_margin_panel(
    margins: Sequence[float | None],
    delta: float | None,
) -> str:
    """Classify a complete frozen panel using the metric-sheet vocabulary."""

    if delta is None or not margins or any(value is None for value in margins):
        return "resolution_unknown"
    band = _finite_number(delta, context="calibrated delta")
    if band < 0.0:
        raise ContractError("calibrated delta cannot be negative")
    values = [_finite_number(value, context="normalized margin") for value in margins]
    positive = [value > band for value in values]
    negative = [value < -band for value in values]
    if all(positive):
        return "robust_aligned"
    if all(negative):
        return "robust_counter"
    if any(positive) and any(negative):
        return "mixed_direction"
    if any(positive):
        return "narrow_aligned"
    if any(negative):
        return "narrow_counter"
    return "resolution_limited"


def evaluate_numeric_rule(
    rule: str,
    margins: Sequence[float | None],
    delta: float | None,
) -> str:
    """Evaluate a preregistered numerical control as pass/ambiguous/fail."""

    if rule not in {"invariant", "different_unsigned", "aligned_all", "access_relation_retained"}:
        raise ContractError("rule requires a non-numeric or unknown evaluator")
    if delta is None or not margins or any(value is None for value in margins):
        return "ambiguous"
    band = _finite_number(delta, context="calibrated delta")
    values = [_finite_number(value, context="control margin") for value in margins]
    if rule == "invariant":
        return "pass" if all(abs(value) <= band for value in values) else "fail"
    if rule == "different_unsigned":
        divergent = [abs(value) > band for value in values]
        if all(divergent):
            return "pass"
        if not any(divergent):
            return "fail"
        return "ambiguous"
    if rule == "aligned_all":
        if all(value > band for value in values):
            return "pass"
        if any(value < -band for value in values) or not any(value > band for value in values):
            return "fail"
        return "ambiguous"

    if len(values) != 3:
        raise ContractError("access retention requires exactly three seed margins per order")
    aligned = sum(value > band for value in values)
    if any(value < -band for value in values) or aligned == 0:
        return "fail"
    if aligned >= 2:
        return "pass"
    return "ambiguous"
