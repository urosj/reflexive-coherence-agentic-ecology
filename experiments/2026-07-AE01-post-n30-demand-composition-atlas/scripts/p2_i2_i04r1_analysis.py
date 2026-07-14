"""Pure corrected measurement analysis for P2-I2 I04-R1.

This module has no PyGRC dependency and performs no file I/O.  It validates
future registered response records, derives rather than trusts causal-chain
status, and keeps every scientific result mode-indexed.  I04-R1 itself only
unit-tests these pure functions; it does not execute a null or a candidate.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
import math
import re
from typing import Any

from ae01_tooling import ContractError


MODES = ("state_carried", "history_carried", "hybrid")
PHYSICAL_ORDERS = ("q1_then_q2", "q2_then_q1")
SCIENTIFIC_STATUSES = ("observed_response", "scientific_no_response")
OPERATIONAL_STATUSES = (
    "censored_runtime",
    "missing_infrastructure",
    "blocked_by_control",
    "invalid_window_protocol",
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
SCHEDULED_STEP_KINDS = ("packet_departure", "packet_arrival")
NO_RESPONSE_STEP_KINDS = ("event_queue_empty", "event_queue_empty")
FORBIDDEN_RESPONSE_PHASE_CALLS = (
    "rcae.schedule_packet_departure",
    "adapter.schedule_response",
    "adapter.read_response_target",
    "controller.read_contributor_slots",
    "controller.author_success",
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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


def _nonempty_string(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{context} must be a non-empty string")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, context: str) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        unknown = sorted(set(value) - expected)
        raise ContractError(f"{context} fields drifted; missing={missing}, unknown={unknown}")


def validate_analysis_policy(policy: Mapping[str, Any]) -> None:
    """Fail closed when a load-bearing I04-R1 analysis choice drifts."""

    if policy.get("policy_id") != "rcae-p2-i2-i04r1-three-mode-analysis-policy-v2":
        raise ContractError("P2-I2 I04-R1 analysis policy identity drifted")
    if policy.get("schema_version") != "1.0.0":
        raise ContractError("analysis policy schema drifted")
    if tuple(policy.get("required_modes", ())) != MODES:
        raise ContractError("all three modes must remain retained in order")

    measurement = policy.get("measurement")
    if not isinstance(measurement, Mapping):
        raise ContractError("measurement policy missing")
    if measurement.get("response_id") != "fixed_window_native_B_target_coherence_gain":
        raise ContractError("downstream response identity drifted")
    if measurement.get("unit") != "native_coherence_amount":
        raise ContractError("response unit drifted")
    if measurement.get("orientation_transform") != "identity":
        raise ContractError("response orientation drifted")
    if measurement.get("value_semantics") != (
        "0 or one fixed registered response-packet amount; this measures native "
        "response scheduling-and-arrival occurrence rather than graded magnitude"
    ):
        raise ContractError("binary-like response semantics drifted")
    window = measurement.get("window_protocol")
    if not isinstance(window, Mapping):
        raise ContractError("fixed response-window protocol missing")
    if window.get("protocol_id") != "p2-i2-native-response-window-v2":
        raise ContractError("response-window identity drifted")
    if window.get("operation_slots") != [
        "capture_B_before_and_empty_queue_identities",
        "emit_feedback_eligibility_surface_row_once",
        "produce_feedback_eligibility_events_once",
        "step_once",
        "step_once",
        "capture_B_after_queue_identities_and_event_lineage",
    ]:
        raise ContractError("outcome-independent response-window slots drifted")
    if (
        window.get("feedback_surface_calls") != 1
        or window.get("producer_calls") != 1
        or window.get("step_calls") != 2
        or tuple(window.get("scheduled_step_kinds", ())) != SCHEDULED_STEP_KINDS
        or tuple(window.get("unscheduled_or_native_block_step_kinds", ()))
        != NO_RESPONSE_STEP_KINDS
        or window.get("outcome_independent_endpoint") is not True
    ):
        raise ContractError("fixed response-window operation counts drifted")
    if len(measurement.get("purity_preconditions", ())) != 5 or len(
        measurement.get("purity_postconditions", ())
    ) != 4:
        raise ContractError("B-purity obligations drifted")

    pairing = policy.get("primary_pairing")
    if not isinstance(pairing, Mapping):
        raise ContractError("primary pairing missing")
    if (
        pairing.get("candidate_cell") != "combined-orders"
        or pairing.get("comparator_cell") != "contributor-removal"
        or pairing.get("comparator_id")
        != "strongest_symmetric_leave_one_common_carrier_admission"
        or tuple(pairing.get("physical_order_strata", ())) != PHYSICAL_ORDERS
        or pairing.get("derived_comparator")
        != "maximum oriented response of both leave-one branches within mode, seed, and physical order"
        or pairing.get("derived_primary_margins_per_mode") != 6
    ):
        raise ContractError("corrected primary comparator drifted")
    branches = pairing.get("leave_one_branches")
    if not isinstance(branches, list) or [row.get("branch_id") for row in branches] != [
        "q1_admitted_q2_diverted",
        "q2_admitted_q1_diverted",
    ]:
        raise ContractError("both symmetric leave-one branches are required")

    diagnostic = policy.get("quantity_matched_scope_diagnostic")
    if not isinstance(diagnostic, Mapping):
        raise ContractError("quantity-matched scope diagnostic missing")
    if (
        diagnostic.get("diagnostic_id")
        != "symmetric_quantity_matched_single_source_repetition"
        or diagnostic.get("repeating_sources") != ["S1", "S2"]
        or tuple(diagnostic.get("physical_order_strata", ())) != PHYSICAL_ORDERS
        or diagnostic.get("not_primary_metric") is not True
        or "equivalence" not in str(diagnostic.get("R03_effect"))
    ):
        raise ContractError("scope-diagnostic symmetry or non-failing status drifted")

    aggregation = policy.get("aggregation_and_missingness")
    if not isinstance(aggregation, Mapping):
        raise ContractError("aggregation and missingness policy missing")
    if aggregation.get("candidate_seeds") != [101, 211, 307]:
        raise ContractError("candidate seeds drifted")
    if tuple(aggregation.get("scientific_statuses", ())) != SCIENTIFIC_STATUSES:
        raise ContractError("scientific status vocabulary drifted")
    if tuple(aggregation.get("operational_statuses", ())) != OPERATIONAL_STATUSES:
        raise ContractError("operational status vocabulary drifted")

    margin = policy.get("paired_margin")
    if not isinstance(margin, Mapping) or margin.get("analysis_arithmetic_floor") != 1e-12:
        raise ContractError("analysis-arithmetic floor drifted")
    if margin.get("runtime_tolerance_source") != (
        "none; all runtime and continuation tolerances are separate I06 registrations"
    ):
        raise ContractError("analytic and runtime resolution boundaries were merged")

    numeric = policy.get("I06_numeric_admissibility")
    if not isinstance(numeric, Mapping):
        raise ContractError("I06 numerical admissibility policy missing")
    if numeric.get("raw_floor") != 1e-12 or numeric.get("binary_safety_factor") != 1024:
        raise ContractError("I06 numerical safety domain drifted")

    classifier = policy.get("relation_classifier")
    if not isinstance(classifier, Mapping):
        raise ContractError("relation classifier missing")
    if classifier.get("delta_name") != "analysis_arithmetic_delta":
        raise ContractError("analytic delta identity drifted")
    if "never by itself" not in str(classifier.get("causal_failure_separation")):
        raise ContractError("metric and causal-failure dispositions were merged")

    causal = policy.get("causal_chain_evidence")
    if not isinstance(causal, Mapping):
        raise ContractError("causal-chain evidence policy missing")
    if causal.get("authored_summary_booleans_authoritative") is not False:
        raise ContractError("authored causal-summary booleans cannot be authoritative")
    if tuple(causal.get("forbidden_response_phase_calls", ())) != FORBIDDEN_RESPONSE_PHASE_CALLS:
        raise ContractError("forbidden response-phase call vocabulary drifted")

    vocabulary = policy.get("machine_rule_vocabulary")
    if not isinstance(vocabulary, Mapping) or set(vocabulary) != {
        "invariant",
        "different_unsigned",
        "aligned_all",
        "raw_visibility",
        "primary_relation",
        "scope_diagnostic",
        "causal_chain_derived",
        "access_relation_retained",
    }:
        raise ContractError("machine-rule vocabulary drifted")

    isolation = policy.get("mode_isolation")
    if not isinstance(isolation, Mapping):
        raise ContractError("mode-isolation policy missing")
    if (
        isolation.get("cross_mode_pooling_averaging_compensation_or_drop") is not False
        or isolation.get("analysis_entrypoint_accepts_exactly_one_mode") is not True
        or len(isolation.get("independent_per_mode", ())) != 7
    ):
        raise ContractError("mode-isolation boundary drifted")
    mode_rules = policy.get("mode_control_rules")
    if not isinstance(mode_rules, Mapping) or tuple(mode_rules) != MODES:
        raise ContractError("mode-specific control registry drifted")
    if [len(mode_rules[mode]) for mode in MODES] != [3, 3, 5]:
        raise ContractError("mode-specific control counts drifted")
    common_rules = policy.get("common_control_rules")
    if not isinstance(common_rules, list) or [row.get("control_id") for row in common_rules] != [
        "each_original_source_alone",
        "pure_source_label_permutation",
        "contribution_operation_reassignment",
        "symmetric_leave_one_common_carrier_admission",
        "pool_write_diversion_or_freeze",
        "private_partition_substitution",
        "direct_or_controller_substitution",
        "quantity_matched_single_source_repetition",
        "alternate_eligible_responder",
    ]:
        raise ContractError("nine corrected common control rules are required")
    if [row.get("control_id") for row in mode_rules["state_carried"]] != [
        "equal_P_order_and_shuffle",
        "post_write_P_debit",
        "audit_history_only_change",
    ]:
        raise ContractError("state-carried machine rules drifted")
    if [row.get("control_id") for row in mode_rules["history_carried"]] != [
        "active_history_order_reversal",
        "P_only_debit_with_H_P_M_H_fixed",
        "H_P_reference_clamp_with_P_fixed",
    ]:
        raise ContractError("history-carried machine rules drifted")
    if [row.get("control_id") for row in mode_rules["hybrid"]] != [
        "complete_P_by_H_P_component_factorial",
        "P_only_reference_intervention",
        "H_P_only_reference_intervention",
        "history_order_reversal_with_P_fixed",
        "interaction_or_synergy",
    ]:
        raise ContractError("hybrid machine rules drifted")
    permitted_rules = set(vocabulary)
    all_rules = common_rules + [row for mode in MODES for row in mode_rules[mode]]
    if any(
        not isinstance(row, Mapping)
        or row.get("rule") not in permitted_rules
        or not isinstance(row.get("cell"), str)
        for row in all_rules
    ):
        raise ContractError("control rule or cell is not machine-defined")

    terminal = policy.get("terminal_input_boundary")
    if not isinstance(terminal, Mapping):
        raise ContractError("terminal input boundary missing")
    if (
        terminal.get("terminal_classification_deferred") is not True
        or terminal.get("mode_selection_or_ranking_forbidden") is not True
    ):
        raise ContractError("I04-R1 cannot classify or rank retained modes")


_RESPONSE_FIELDS = {
    "record_id",
    "mode",
    "seed",
    "physical_order_id",
    "cell_id",
    "branch_id",
    "pairing_identity",
    "opportunity_id",
    "response_id",
    "unit",
    "status",
    "B_before",
    "B_after",
    "raw_response",
    "oriented_response",
    "carrier_state_digest",
    "window_protocol_id",
    "pre_packet_queue_length",
    "pre_birth_queue_length",
    "post_packet_queue_length",
    "post_birth_queue_length",
    "feedback_surface_call_count",
    "producer_call_count",
    "step_call_count",
    "step_processed_event_kinds",
    "producer_reason",
    "response_packet_id",
    "departure_event_id",
    "arrival_event_id",
    "response_packet_amount",
    "runtime_tolerance",
    "B_targeting_event_ids",
    "native_chain_evidence_refs",
    "operational_failure_id",
}


def validate_response_record(record: Mapping[str, Any]) -> None:
    """Validate one response without trusting an authored success flag."""

    _exact_keys(record, _RESPONSE_FIELDS, context="response record")
    if record["mode"] not in MODES:
        raise ContractError("response mode is not retained")
    if record["physical_order_id"] not in PHYSICAL_ORDERS:
        raise ContractError("physical q-order is invalid")
    if record["response_id"] != "fixed_window_native_B_target_coherence_gain":
        raise ContractError("response identity drifted")
    if record["unit"] != "native_coherence_amount":
        raise ContractError("response unit drifted")
    if not isinstance(record["seed"], int) or isinstance(record["seed"], bool):
        raise ContractError("response seed must be an integer")
    for field in (
        "record_id",
        "cell_id",
        "branch_id",
        "pairing_identity",
        "opportunity_id",
        "carrier_state_digest",
        "producer_reason",
    ):
        _nonempty_string(record[field], context=field)
    if record["window_protocol_id"] != "p2-i2-native-response-window-v2":
        raise ContractError("response used the wrong fixed window")
    for field in (
        "pre_packet_queue_length",
        "pre_birth_queue_length",
        "post_packet_queue_length",
        "post_birth_queue_length",
        "feedback_surface_call_count",
        "producer_call_count",
        "step_call_count",
    ):
        if not isinstance(record[field], int) or isinstance(record[field], bool) or record[field] < 0:
            raise ContractError(f"{field} must be a nonnegative integer")
    kinds = record["step_processed_event_kinds"]
    if not isinstance(kinds, list) or any(not isinstance(item, str) for item in kinds):
        raise ContractError("step event kinds must be a string list")
    targeting = record["B_targeting_event_ids"]
    if not isinstance(targeting, list) or any(
        not isinstance(item, str) or not item for item in targeting
    ):
        raise ContractError("B-targeting event IDs must be a string list")
    refs = record["native_chain_evidence_refs"]
    if not isinstance(refs, list) or any(not isinstance(item, str) or not item for item in refs):
        raise ContractError("native-chain evidence refs must be a string list")

    status = record["status"]
    if status in SCIENTIFIC_STATUSES:
        before = _finite_number(record["B_before"], context="B_before")
        after = _finite_number(record["B_after"], context="B_after")
        raw = _finite_number(record["raw_response"], context="raw response")
        oriented = _finite_number(record["oriented_response"], context="oriented response")
        tolerance = _finite_number(record["runtime_tolerance"], context="runtime tolerance")
        if before < 0.0 or after < 0.0 or raw < 0.0:
            raise ContractError("native coherence responses must be nonnegative")
        if tolerance < 0.0:
            raise ContractError("runtime tolerance must be nonnegative")
        if raw != after - before or oriented != raw:
            raise ContractError("response must be the identity-oriented B_after-B_before gain")
        if (
            record["pre_packet_queue_length"] != 0
            or record["pre_birth_queue_length"] != 0
            or record["post_packet_queue_length"] != 0
            or record["post_birth_queue_length"] != 0
            or record["feedback_surface_call_count"] != 1
            or record["producer_call_count"] != 1
            or record["step_call_count"] != 2
        ):
            raise ContractError("scientific response violates fixed-window counts or B-purity queues")
        if record["operational_failure_id"] is not None:
            raise ContractError("scientific response cannot carry an operational failure")
        if status == "observed_response":
            amount = _finite_number(record["response_packet_amount"], context="packet amount")
            packet_id = _nonempty_string(record["response_packet_id"], context="response packet ID")
            departure_id = _nonempty_string(record["departure_event_id"], context="departure event ID")
            arrival_id = _nonempty_string(record["arrival_event_id"], context="arrival event ID")
            if (
                amount <= 0.0
                or abs(raw - amount) > tolerance
                or tolerance >= amount / 1024
            ):
                raise ContractError(
                    "observed gain must equal one positive fixed response packet within its separately registered tolerance"
                )
            if tuple(kinds) != SCHEDULED_STEP_KINDS:
                raise ContractError("observed response must process departure then arrival")
            if targeting != [arrival_id] or len(refs) < 3:
                raise ContractError("observed response lacks unique B-arrival lineage")
            if len({packet_id, departure_id, arrival_id}) != 3:
                raise ContractError("packet and event identities must be distinct")
        else:
            if raw != 0.0 or tuple(kinds) != NO_RESPONSE_STEP_KINDS:
                raise ContractError("scientific no-response requires a complete empty two-step window")
            if any(
                record[field] is not None
                for field in (
                    "response_packet_id",
                    "departure_event_id",
                    "arrival_event_id",
                    "response_packet_amount",
                )
            ) or targeting or refs:
                raise ContractError("scientific no-response cannot retain response lineage")
    elif status in OPERATIONAL_STATUSES:
        tolerance = _finite_number(record["runtime_tolerance"], context="runtime tolerance")
        if tolerance < 0.0:
            raise ContractError("runtime tolerance must be nonnegative")
        if any(
            record[field] is not None
            for field in ("B_after", "raw_response", "oriented_response")
        ):
            raise ContractError("operationally incomplete response values must be null")
        _finite_number(record["B_before"], context="operational B_before")
        _nonempty_string(record["operational_failure_id"], context="operational failure ID")
    else:
        raise ContractError("unknown response status")


def normalized_paired_difference(candidate: float, comparator: float, floor: float) -> float:
    """Return the corrected oriented normalized difference."""

    left = _finite_number(candidate, context="candidate response")
    right = _finite_number(comparator, context="comparator response")
    denominator_floor = _finite_number(floor, context="analysis-arithmetic floor")
    if left < 0.0 or right < 0.0 or denominator_floor <= 0.0:
        raise ContractError("responses must be nonnegative and floor positive")
    return (left - right) / max(abs(left), abs(right), denominator_floor)


def _paired_records(records: Sequence[Mapping[str, Any]]) -> list[str]:
    for record in records:
        validate_response_record(record)
    fields = (
        "mode",
        "seed",
        "physical_order_id",
        "pairing_identity",
        "opportunity_id",
        "window_protocol_id",
        "B_before",
    )
    return [
        field
        for field in fields
        if any(record[field] != records[0][field] for record in records[1:])
    ]


def primary_margin(
    candidate: Mapping[str, Any],
    q1_only: Mapping[str, Any],
    q2_only: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare a candidate to the stronger of two symmetric leave-one arms."""

    validate_analysis_policy(policy)
    drift = _paired_records((candidate, q1_only, q2_only))
    if drift:
        raise ContractError(f"primary pairing identity drifted: {drift}")
    expected = (
        (candidate, "combined-orders"),
        (q1_only, "q1_admitted_q2_diverted"),
        (q2_only, "q2_admitted_q1_diverted"),
    )
    if any(record["branch_id"] != branch for record, branch in expected):
        raise ContractError("primary branch identities drifted")
    digests = {record["carrier_state_digest"] for record in (candidate, q1_only, q2_only)}
    if len(digests) != 3:
        raise ContractError("primary comparator must change each common-carrier state")

    evaluable = all(record["status"] in SCIENTIFIC_STATUSES for record in expected_record_set(expected))
    selected: Mapping[str, Any] | None = None
    margin: float | None = None
    strongest: float | None = None
    if evaluable:
        # q1 wins exact ties; the rule is frozen and never selected by effect size.
        selected = q1_only if q1_only["oriented_response"] >= q2_only["oriented_response"] else q2_only
        strongest = float(selected["oriented_response"])
        margin = normalized_paired_difference(
            float(candidate["oriented_response"]),
            strongest,
            float(policy["paired_margin"]["analysis_arithmetic_floor"]),
        )
    return {
        "mode": candidate["mode"],
        "seed": candidate["seed"],
        "physical_order_id": candidate["physical_order_id"],
        "pairing_identity": candidate["pairing_identity"],
        "candidate_record_id": candidate["record_id"],
        "q1_only_record_id": q1_only["record_id"],
        "q2_only_record_id": q2_only["record_id"],
        "candidate_response": candidate["oriented_response"],
        "q1_only_response": q1_only["oriented_response"],
        "q2_only_response": q2_only["oriented_response"],
        "selected_comparator_record_id": None if selected is None else selected["record_id"],
        "strongest_leave_one_response": strongest,
        "evaluable": evaluable,
        "normalized_margin": margin,
    }


def expected_record_set(
    rows: Sequence[tuple[Mapping[str, Any], str]],
) -> tuple[Mapping[str, Any], ...]:
    """Keep the record extraction explicit for static audit and typing."""

    return tuple(record for record, _ in rows)


def classify_margin_panel(margins: Sequence[float | None], delta: float | None) -> str:
    """Classify a complete frozen panel using the L02 relation vocabulary."""

    if delta is None or not margins or any(value is None for value in margins):
        return "resolution_unknown"
    band = _finite_number(delta, context="analysis-arithmetic delta")
    if band < 0.0:
        raise ContractError("analysis-arithmetic delta cannot be negative")
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
    """Evaluate a frozen numerical control as pass/ambiguous/fail."""

    if rule not in {"invariant", "different_unsigned", "aligned_all", "access_relation_retained"}:
        raise ContractError("rule requires a non-numeric or unknown evaluator")
    if delta is None or not margins or any(value is None for value in margins):
        return "ambiguous"
    band = _finite_number(delta, context="analysis-arithmetic delta")
    if band < 0.0:
        raise ContractError("analysis-arithmetic delta cannot be negative")
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


def analyze_mode_primary(
    mode: str,
    primary_rows: Sequence[Mapping[str, Any]],
    delta: float | None,
    *,
    op08_disposition: str,
) -> dict[str, Any]:
    """Analyze exactly one mode; never pool or compensate across modes."""

    if mode not in MODES:
        raise ContractError("mode is not retained")
    if op08_disposition not in {"pass", "ambiguous", "fail"}:
        raise ContractError("OP-08 disposition is invalid")
    if len(primary_rows) != 6:
        raise ContractError("one mode requires exactly six primary margins")
    expected_pairs = {(seed, order) for seed in (101, 211, 307) for order in PHYSICAL_ORDERS}
    actual_pairs: set[tuple[int, str]] = set()
    for row in primary_rows:
        if row.get("mode") != mode:
            raise ContractError("cross-mode input is forbidden")
        pair = (row.get("seed"), row.get("physical_order_id"))
        if pair in actual_pairs:
            raise ContractError("duplicate mode/seed/order primary margin")
        actual_pairs.add(pair)
    if actual_pairs != expected_pairs:
        raise ContractError("mode primary panel does not cover the frozen seeds and orders")

    order_relations: dict[str, str] = {}
    for order in PHYSICAL_ORDERS:
        rows = sorted(
            (row for row in primary_rows if row["physical_order_id"] == order),
            key=lambda row: row["seed"],
        )
        order_relations[order] = classify_margin_panel(
            [row.get("normalized_margin") for row in rows], delta
        )
    relations = tuple(order_relations[order] for order in PHYSICAL_ORDERS)
    if relations == ("robust_aligned", "robust_aligned"):
        signature = "top_aligned"
    elif (
        op08_disposition == "pass"
        and relations[0] != relations[1]
        and any(value not in {"resolution_limited", "resolution_unknown"} for value in relations)
    ):
        signature = "order_conditioned_or_mixed"
    elif "resolution_unknown" in relations:
        signature = "unresolved"
    else:
        signature = "not_top_no_causal_disposition"
    return {
        "mode": mode,
        "per_order_relation": order_relations,
        "mode_metric_signature": signature,
        "op08_disposition": op08_disposition,
        "causal_failure_derived": False,
        "causal_failure_note": "metric signature alone never assigns mode-hypothesis failure",
    }


def evaluate_quantity_scope_diagnostic(
    candidate: Mapping[str, Any],
    repeated_s1: Mapping[str, Any],
    repeated_s2: Mapping[str, Any],
    delta: float | None,
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Retain both repeated-source arms; equivalence never fails R03."""

    validate_analysis_policy(policy)
    drift = _paired_records((candidate, repeated_s1, repeated_s2))
    if drift:
        raise ContractError(f"scope-diagnostic pairing identity drifted: {drift}")
    if repeated_s1["branch_id"] != "quantity_matched_repeated_S1" or repeated_s2[
        "branch_id"
    ] != "quantity_matched_repeated_S2":
        raise ContractError("both symmetric repeated-source branches are required")
    evaluable = all(
        record["status"] in SCIENTIFIC_STATUSES for record in (candidate, repeated_s1, repeated_s2)
    )
    margins: dict[str, float | None] = {"S1": None, "S2": None}
    relation = "resolution_unknown"
    if evaluable:
        floor = float(policy["paired_margin"]["analysis_arithmetic_floor"])
        margins = {
            "S1": normalized_paired_difference(
                float(candidate["oriented_response"]), float(repeated_s1["oriented_response"]), floor
            ),
            "S2": normalized_paired_difference(
                float(candidate["oriented_response"]), float(repeated_s2["oriented_response"]), floor
            ),
        }
        relation = classify_margin_panel(tuple(margins.values()), delta)
    carrier_matches = {
        "S1": candidate["carrier_state_digest"] == repeated_s1["carrier_state_digest"],
        "S2": candidate["carrier_state_digest"] == repeated_s2["carrier_state_digest"],
    }
    if evaluable and all(carrier_matches.values()) and relation == "resolution_limited":
        scope_reading = "source_label_invariant_equivalence"
    elif evaluable and all(carrier_matches.values()):
        scope_reading = "carrier_matched_response_divergence"
    elif evaluable:
        scope_reading = "carrier_not_matched_scope_qualified"
    else:
        scope_reading = "resolution_unknown"
    return {
        "mode": candidate["mode"],
        "seed": candidate["seed"],
        "physical_order_id": candidate["physical_order_id"],
        "candidate_record_id": candidate["record_id"],
        "repeated_S1_record_id": repeated_s1["record_id"],
        "repeated_S2_record_id": repeated_s2["record_id"],
        "carrier_matches_candidate": carrier_matches,
        "normalized_margins": margins,
        "metric_relation": relation,
        "scope_reading": scope_reading,
        "R03_failure": False,
        "R03_note": "numerical equivalence alone has no R03 effect",
    }


def validate_numeric_admissibility(
    B_before: float,
    response_amount: float,
    runtime_tolerance: float,
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate an I06 binary response against the frozen analytic domain."""

    validate_analysis_policy(policy)
    baseline = _finite_number(B_before, context="B_before")
    amount = _finite_number(response_amount, context="response amount")
    tolerance = _finite_number(runtime_tolerance, context="runtime tolerance")
    if baseline < 0.0 or amount <= 0.0 or tolerance < 0.0:
        raise ContractError("B baseline/tolerance must be nonnegative and response amount positive")
    after = baseline + amount
    if not math.isfinite(after):
        raise ContractError("B_before + response amount must be finite")
    roundtrip = json.loads(json.dumps({"B_before": baseline, "r": amount, "B_after": after}))
    if roundtrip != {"B_before": baseline, "r": amount, "B_after": after}:
        raise ContractError("numerical values are not canonical-JSON round-trippable")
    numeric = policy["I06_numeric_admissibility"]
    factor = int(numeric["binary_safety_factor"])
    floor = float(numeric["raw_floor"])
    ulp_bound = factor * max(math.ulp(baseline), math.ulp(after))
    floor_bound = factor * floor
    admissible = (
        amount >= floor_bound
        and amount >= ulp_bound
        and after - baseline > 0.0
        and tolerance < amount / factor
    )
    return {
        "admissible": admissible,
        "B_before": baseline,
        "response_amount": amount,
        "B_after": after,
        "floor_bound": floor_bound,
        "ulp_bound": ulp_bound,
        "runtime_tolerance_bound": amount / factor,
        "runtime_tolerance": tolerance,
    }


_CAUSAL_FIELDS = {
    "evidence_id",
    "branch_id",
    "branch_kind",
    "mode",
    "common_carrier_id",
    "common_carrier_mask",
    "private_partitions",
    "contribution_arrivals",
    "response_actor_id",
    "response_target_id",
    "response_front_masks",
    "call_records",
    "producer_records",
    "packet_event_records",
    "branch_configuration_sha256",
    "runtime_binding_receipt_sha256",
    "call_trace_sha256",
}


def _string_set(value: Any, *, context: str, allow_empty: bool = False) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ContractError(f"{context} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise ContractError(f"{context} cannot contain duplicates")
    if not value and not allow_empty:
        raise ContractError(f"{context} cannot be empty")
    return set(value)


def derive_causal_chain_status(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Derive candidate/substitute status solely from retained provenance."""

    _exact_keys(evidence, _CAUSAL_FIELDS, context="causal-chain evidence")
    if evidence["mode"] not in MODES:
        raise ContractError("causal evidence mode is not retained")
    kind = evidence["branch_kind"]
    if kind not in {"candidate", "private_substitution", "controller_substitution"}:
        raise ContractError("unknown causal branch kind")
    for field in (
        "evidence_id",
        "branch_id",
        "common_carrier_id",
        "response_actor_id",
        "response_target_id",
    ):
        _nonempty_string(evidence[field], context=field)
    for field in (
        "branch_configuration_sha256",
        "runtime_binding_receipt_sha256",
        "call_trace_sha256",
    ):
        if not isinstance(evidence[field], str) or not _SHA256_RE.fullmatch(evidence[field]):
            raise ContractError(f"{field} must be a lowercase SHA-256")

    common_mask = _string_set(evidence["common_carrier_mask"], context="common carrier mask")
    partitions: list[set[str]] = []
    if not isinstance(evidence["private_partitions"], list):
        raise ContractError("private partitions must be a list")
    for row in evidence["private_partitions"]:
        if not isinstance(row, Mapping) or set(row) != {"partition_id", "member_ids"}:
            raise ContractError("private partition fields drifted")
        _nonempty_string(row["partition_id"], context="private partition ID")
        partitions.append(_string_set(row["member_ids"], context="private partition members"))
    if any(left & right for index, left in enumerate(partitions) for right in partitions[index + 1 :]):
        raise ContractError("private partitions must be disjoint")

    arrivals = evidence["contribution_arrivals"]
    if not isinstance(arrivals, list):
        raise ContractError("contribution arrivals must be a list")
    for row in arrivals:
        if not isinstance(row, Mapping) or set(row) != {"source_role", "target_carrier_id", "event_id"}:
            raise ContractError("contribution-arrival fields drifted")
        for value in row.values():
            _nonempty_string(value, context="contribution-arrival value")

    masks = evidence["response_front_masks"]
    if not isinstance(masks, list):
        raise ContractError("response front masks must be a list")
    parsed_masks: list[set[str]] = []
    for row in masks:
        if not isinstance(row, Mapping) or set(row) != {"actor_id", "carrier_ids"}:
            raise ContractError("response front-mask fields drifted")
        _nonempty_string(row["actor_id"], context="front-mask actor")
        parsed_masks.append(_string_set(row["carrier_ids"], context="response front mask"))

    calls = evidence["call_records"]
    if not isinstance(calls, list):
        raise ContractError("call records must be a list")
    forbidden_calls: list[str] = []
    contributor_addressed_inputs = False
    for row in calls:
        if not isinstance(row, Mapping) or set(row) != {
            "phase",
            "actor",
            "callable",
            "input_carrier_ids",
        }:
            raise ContractError("call-record fields drifted")
        for field in ("phase", "actor", "callable"):
            _nonempty_string(row[field], context=f"call {field}")
        inputs = _string_set(row["input_carrier_ids"], context="call inputs", allow_empty=True)
        if row["phase"] == "response":
            if row["callable"] in FORBIDDEN_RESPONSE_PHASE_CALLS:
                forbidden_calls.append(row["callable"])
            if {"S1", "S2"} & inputs:
                contributor_addressed_inputs = True

    producers = evidence["producer_records"]
    if not isinstance(producers, list):
        raise ContractError("producer records must be a list")
    for row in producers:
        if not isinstance(row, Mapping) or set(row) != {
            "producer_record_id",
            "feedback_row_id",
            "packet_id",
        }:
            raise ContractError("producer-record fields drifted")
        for value in row.values():
            _nonempty_string(value, context="producer-record value")

    events = evidence["packet_event_records"]
    if not isinstance(events, list):
        raise ContractError("packet event records must be a list")
    for row in events:
        if not isinstance(row, Mapping) or set(row) != {
            "event_id",
            "kind",
            "packet_id",
            "source_id",
            "target_id",
        }:
            raise ContractError("packet-event fields drifted")
        for value in row.values():
            _nonempty_string(value, context="packet-event value")

    source_roles = {row["source_role"] for row in arrivals}
    arrivals_to_common = all(
        row["target_carrier_id"] == evidence["common_carrier_id"] for row in arrivals
    )
    front_is_common = len(parsed_masks) == 1 and parsed_masks[0] == common_mask
    private_union = set().union(*partitions) if partitions else set()
    no_private_or_source_crossread = not (common_mask & private_union) and not (
        common_mask & {"S1", "S2"}
    )
    native_link = False
    if len(producers) == 1 and len(events) == 2:
        producer = producers[0]
        departure = [row for row in events if row["kind"] == "packet_departure"]
        arrival = [row for row in events if row["kind"] == "packet_arrival"]
        native_link = (
            len(departure) == 1
            and len(arrival) == 1
            and producer["packet_id"] == departure[0]["packet_id"] == arrival[0]["packet_id"]
            and departure[0]["source_id"] == evidence["response_actor_id"]
            and departure[0]["target_id"] == evidence["response_target_id"]
            and arrival[0]["source_id"] == evidence["response_actor_id"]
            and arrival[0]["target_id"] == evidence["response_target_id"]
        )

    if kind == "candidate":
        derived = (
            source_roles == {"S1", "S2"}
            and len(arrivals) == 2
            and arrivals_to_common
            and front_is_common
            and no_private_or_source_crossread
            and native_link
            and not forbidden_calls
            and not contributor_addressed_inputs
        )
        status = "valid_common_carrier" if derived else "invalid_common_carrier"
    elif kind == "private_substitution":
        masks_each_private = bool(parsed_masks) and all(
            sum(mask <= partition for partition in partitions) == 1 for mask in parsed_masks
        )
        no_common_aggregate = all(mask != common_mask for mask in parsed_masks)
        derived = masks_each_private and no_common_aggregate
        status = "private_partition_excluded" if derived else "private_exclusion_unproven"
    else:
        derived = bool(forbidden_calls or contributor_addressed_inputs)
        status = "controller_bypass_excluded" if derived else "controller_exclusion_unproven"

    return {
        "evidence_id": evidence["evidence_id"],
        "branch_kind": kind,
        "derived_status": status,
        "machine_disposition": "pass" if derived else "fail",
        "derived_facts": {
            "source_roles": sorted(source_roles),
            "all_contribution_arrivals_target_common_carrier": arrivals_to_common,
            "response_front_equals_common_mask": front_is_common,
            "native_packet_lineage_complete": native_link,
            "forbidden_response_phase_calls": sorted(set(forbidden_calls)),
            "contributor_addressed_response_input": contributor_addressed_inputs,
        },
    }
