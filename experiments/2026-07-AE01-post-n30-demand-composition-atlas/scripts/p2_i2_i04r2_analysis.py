"""Conditional machine-invariant layer over the accepted P2-I2 I04-R1 analysis.

The I04-R1 artifacts remain immutable historical inputs.  This pure module
adds window/arrival receipts and exposes the exact three-arm primary estimator
that both future live analysis and the future I05 arithmetic null must use.
It performs no file I/O and imports no PyGRC code.
"""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import math
import re
from typing import Any

from ae01_tooling import ContractError
import p2_i2_i04r1_analysis as base


MODES = base.MODES
PHYSICAL_ORDERS = base.PHYSICAL_ORDERS
SCIENTIFIC_STATUSES = base.SCIENTIFIC_STATUSES
OPERATIONAL_STATUSES = base.OPERATIONAL_STATUSES
ARRIVAL_SOURCE_SHA256 = "14d99292e18e2fe34e0fd5c6a1f69051e82115a051d142f10792775e2321e58f"
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


def _sha256_string(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise ContractError(f"{context} must be a lowercase SHA-256")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], *, context: str) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        unknown = sorted(set(value) - expected)
        raise ContractError(f"{context} fields drifted; missing={missing}, unknown={unknown}")


def validate_machine_policy(
    machine_policy: Mapping[str, Any],
    parent_analysis_policy: Mapping[str, Any],
) -> None:
    """Validate the I04-R2 overlay and its exact I04-R1 semantic parent."""

    base.validate_analysis_policy(parent_analysis_policy)
    if machine_policy.get("policy_id") != "rcae-p2-i2-i04r2-conditional-machine-policy-v1":
        raise ContractError("I04-R2 machine policy identity drifted")
    if machine_policy.get("schema_version") != "1.0.0":
        raise ContractError("I04-R2 machine policy schema drifted")
    if tuple(machine_policy.get("required_modes", ())) != MODES:
        raise ContractError("I04-R2 must retain all three modes in order")
    parent = machine_policy.get("parent_analysis")
    if not isinstance(parent, Mapping) or parent.get("policy_id") != parent_analysis_policy.get(
        "policy_id"
    ):
        raise ContractError("I04-R2 parent analysis identity drifted")
    if parent.get("sha256") != "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d":
        raise ContractError("I04-R1 parent policy SHA-256 drifted")

    evaluator = machine_policy.get("complete_two_arm_evaluability")
    if not isinstance(evaluator, Mapping):
        raise ContractError("complete two-arm evaluability policy missing")
    if (
        evaluator.get("candidate_branch_id") != "combined-orders"
        or evaluator.get("leave_branch_ids")
        != ["q1_admitted_q2_diverted", "q2_admitted_q1_diverted"]
        or evaluator.get("required_scientific_records") != 3
        or evaluator.get("cross_seed_order_or_mode_max_forbidden") is not True
        or evaluator.get("tie_rule") != "q1-only wins exact ties"
    ):
        raise ContractError("complete two-arm or within-tuple max rule drifted")

    null_path = machine_policy.get("I05_exact_estimator_path")
    if not isinstance(null_path, Mapping):
        raise ContractError("I05 exact estimator path missing")
    if (
        null_path.get("precollapsed_comparator_input_forbidden") is not True
        or null_path.get("direct_normalized_difference_call_in_calibration_entrypoint_forbidden")
        is not True
        or "p2_i2_i04r2_analysis.primary_margin" not in null_path.get("route", ())
        or null_path.get("runtime_tolerance_effect") != "none"
    ):
        raise ContractError("future I05 three-arm estimator route drifted")

    diversion = machine_policy.get("I06_diversion_admissibility")
    if not isinstance(diversion, Mapping):
        raise ContractError("I06 diversion admissibility missing")
    if len(diversion.get("must_match", ())) != 10 or len(
        diversion.get("inert_sink_must_not_influence", ())
    ) != 8:
        raise ContractError("I06 diversion matching/noninterference duties drifted")
    if "cannot register" not in str(diversion.get("failure_effect")):
        raise ContractError("I06 diversion failure must block registration")

    arrival = machine_policy.get("I06_arrival_gain_admissibility")
    if not isinstance(arrival, Mapping):
        raise ContractError("I06 arrival-gain admissibility missing")
    if (
        arrival.get("current_arrival_transform_id") != "identity_packet_amount_addition"
        or arrival.get("current_arrival_source", {}).get("sha256") != ARRIVAL_SOURCE_SHA256
        or len(arrival.get("forbidden_adjustment_event_kinds", ())) != 5
        or "reopen I04" not in str(arrival.get("semantic_change_effect"))
    ):
        raise ContractError("native arrival identity/domain boundary drifted")

    window = machine_policy.get("window_before_scientific_zero")
    if not isinstance(window, Mapping):
        raise ContractError("window-before-zero policy missing")
    if (
        window.get("protocol_id") != "p2-i2-native-response-window-v2"
        or len(window.get("required_receipt_fields", ())) != 8
        or "operational null" not in str(window.get("failure_effect"))
    ):
        raise ContractError("window receipt or failure boundary drifted")

    diagnostic = machine_policy.get("non_gating_scope_diagnostic")
    order = machine_policy.get("order_conditioned_classification")
    causal = machine_policy.get("causal_receipt_authority")
    if not isinstance(diagnostic, Mapping) or len(diagnostic.get("forbidden_effects", ())) != 5:
        raise ContractError("non-gating scope-diagnostic policy drifted")
    if not isinstance(order, Mapping) or "not automatic" not in str(order.get("not_top_effect")):
        raise ContractError("order-conditioned classification boundary drifted")
    if (
        not isinstance(causal, Mapping)
        or causal.get("authored_summary_booleans_authoritative") is not False
        or causal.get("output_difference_sufficient") is not False
        or len(causal.get("required_sources", ())) != 8
    ):
        raise ContractError("receipt-derived causal authority drifted")


_ENVELOPE_FIELDS = {
    "i04r1_response_record",
    "window_validity_receipt",
    "arrival_gain_receipt",
}
_WINDOW_FIELDS = {
    "feedback_evaluation_id",
    "feedback_policy_id",
    "producer_invocation_id",
    "producer_invocation_receipt_sha256",
    "pre_queue_identity_sha256",
    "post_queue_identity_sha256",
    "step_processed_event_ids",
    "window_contamination_event_ids",
}
_ARRIVAL_FIELDS = {
    "native_coherence_domain_id",
    "native_coherence_domain_lower",
    "native_coherence_domain_upper",
    "expected_native_arrival_gain",
    "arrival_transform_id",
    "arrival_semantics_source_sha256",
    "arrival_semantics_receipt_sha256",
    "arrival_adjustment_event_ids",
}


def validate_response_envelope(
    envelope: Mapping[str, Any],
    machine_policy: Mapping[str, Any],
    parent_analysis_policy: Mapping[str, Any],
) -> None:
    """Validate the base response only after its window and arrival receipts."""

    validate_machine_policy(machine_policy, parent_analysis_policy)
    _exact_keys(envelope, _ENVELOPE_FIELDS, context="I04-R2 response envelope")
    record = envelope["i04r1_response_record"]
    window = envelope["window_validity_receipt"]
    arrival = envelope["arrival_gain_receipt"]
    if not isinstance(record, Mapping) or not isinstance(window, Mapping) or not isinstance(
        arrival, Mapping
    ):
        raise ContractError("response envelope components must be objects")
    base.validate_response_record(record)

    _exact_keys(window, _WINDOW_FIELDS, context="window validity receipt")
    for field in ("feedback_evaluation_id", "feedback_policy_id", "producer_invocation_id"):
        _nonempty_string(window[field], context=field)
    for field in (
        "producer_invocation_receipt_sha256",
        "pre_queue_identity_sha256",
        "post_queue_identity_sha256",
    ):
        _sha256_string(window[field], context=field)
    step_ids = window["step_processed_event_ids"]
    if not isinstance(step_ids, list) or len(step_ids) != 2 or any(
        item is not None and (not isinstance(item, str) or not item) for item in step_ids
    ):
        raise ContractError("window receipt requires exactly two string-or-null step event IDs")
    contamination = window["window_contamination_event_ids"]
    if not isinstance(contamination, list) or any(
        not isinstance(item, str) or not item for item in contamination
    ):
        raise ContractError("window contamination IDs must be a string list")

    _exact_keys(arrival, _ARRIVAL_FIELDS, context="arrival gain receipt")
    _nonempty_string(arrival["native_coherence_domain_id"], context="native coherence domain ID")
    lower = _finite_number(arrival["native_coherence_domain_lower"], context="domain lower")
    upper = _finite_number(arrival["native_coherence_domain_upper"], context="domain upper")
    if lower > upper:
        raise ContractError("native coherence domain bounds are reversed")
    if arrival["arrival_semantics_source_sha256"] != ARRIVAL_SOURCE_SHA256:
        raise ContractError("arrival semantics source identity drifted")
    _sha256_string(
        arrival["arrival_semantics_receipt_sha256"], context="arrival semantics receipt"
    )
    adjustments = arrival["arrival_adjustment_event_ids"]
    if not isinstance(adjustments, list) or any(
        not isinstance(item, str) or not item for item in adjustments
    ):
        raise ContractError("arrival adjustment event IDs must be a string list")

    status = record["status"]
    scientific = status in SCIENTIFIC_STATUSES
    if scientific:
        before = _finite_number(record["B_before"], context="B_before")
        after = _finite_number(record["B_after"], context="B_after")
        if not (lower <= before <= upper and lower <= after <= upper):
            raise ContractError("B_before/B_after lie outside the registered native coherence domain")
        if contamination:
            raise ContractError("window contamination makes the response operationally invalid")
        if status == "observed_response":
            expected = _finite_number(
                arrival["expected_native_arrival_gain"], context="expected native arrival gain"
            )
            amount = _finite_number(record["response_packet_amount"], context="packet amount")
            tolerance = _finite_number(record["runtime_tolerance"], context="runtime tolerance")
            if (
                arrival["arrival_transform_id"] != "identity_packet_amount_addition"
                or expected != amount
                or expected <= 0.0
                or abs(float(record["raw_response"]) - expected) > tolerance
                or adjustments
            ):
                raise ContractError("observed arrival gain is not one unadjusted identity packet amount")
            if step_ids != [record["departure_event_id"], record["arrival_event_id"]]:
                raise ContractError("observed step event IDs do not match response departure/arrival")
        else:
            if (
                arrival["expected_native_arrival_gain"] != 0.0
                or arrival["arrival_transform_id"] != "no_arrival"
                or adjustments
                or step_ids != [None, None]
            ):
                raise ContractError("scientific zero requires no arrival, adjustment, or processed event")
    elif status in OPERATIONAL_STATUSES:
        if arrival["expected_native_arrival_gain"] is not None:
            raise ContractError("operationally invalid arrival gain must be null")
    else:
        raise ContractError("unknown base response status")


def primary_margin(
    candidate: Mapping[str, Any],
    q1_only: Mapping[str, Any],
    q2_only: Mapping[str, Any],
    machine_policy: Mapping[str, Any],
    parent_analysis_policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Run the one authorized three-arm estimator, all-or-none within tuple."""

    envelopes = (candidate, q1_only, q2_only)
    for envelope in envelopes:
        validate_response_envelope(envelope, machine_policy, parent_analysis_policy)
    records = tuple(envelope["i04r1_response_record"] for envelope in envelopes)
    result = base.primary_margin(*records, parent_analysis_policy)
    invalid_records = [
        record["record_id"] for record in records if record["status"] not in SCIENTIFIC_STATUSES
    ]
    if invalid_records and (
        result["evaluable"]
        or result["selected_comparator_record_id"] is not None
        or result["normalized_margin"] is not None
    ):
        raise ContractError("operationally invalid arm was silently removed before max")
    return {
        **result,
        "complete_three_arm_tuple_valid": not invalid_records,
        "nonevaluable_record_ids": invalid_records,
        "estimator_path_id": "p2-i2-i04r2-exact-three-arm-primary-estimator-v1",
    }


def _synthetic_sha256(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def build_synthetic_response_envelope(
    *,
    record_id: str,
    branch_id: str,
    response: float,
    seed: int,
    physical_order_id: str,
    carrier_state_digest: str,
    pairing_identity: str,
) -> dict[str, Any]:
    """Build one pure I05 arithmetic-null arm; never a runtime observation."""

    value = _finite_number(response, context="synthetic response")
    if value <= 0.0:
        raise ContractError("synthetic arithmetic-null response must be positive")
    packet_id = f"{record_id}-packet"
    departure_id = f"{record_id}-departure"
    arrival_id = f"{record_id}-arrival"
    receipt = _synthetic_sha256(f"I05-pure-receipt:{record_id}")
    return {
        "i04r1_response_record": {
            "record_id": record_id,
            "mode": "state_carried",
            "seed": seed,
            "physical_order_id": physical_order_id,
            "cell_id": "combined-orders" if branch_id == "combined-orders" else "contributor-removal",
            "branch_id": branch_id,
            "pairing_identity": pairing_identity,
            "opportunity_id": "I05-pure-analysis-opportunity",
            "response_id": "fixed_window_native_B_target_coherence_gain",
            "unit": "native_coherence_amount",
            "status": "observed_response",
            "B_before": 0.0,
            "B_after": value,
            "raw_response": value,
            "oriented_response": value,
            "carrier_state_digest": carrier_state_digest,
            "window_protocol_id": "p2-i2-native-response-window-v2",
            "pre_packet_queue_length": 0,
            "pre_birth_queue_length": 0,
            "post_packet_queue_length": 0,
            "post_birth_queue_length": 0,
            "feedback_surface_call_count": 1,
            "producer_call_count": 1,
            "step_call_count": 2,
            "step_processed_event_kinds": ["packet_departure", "packet_arrival"],
            "producer_reason": "synthetic_analysis_scheduled",
            "response_packet_id": packet_id,
            "departure_event_id": departure_id,
            "arrival_event_id": arrival_id,
            "response_packet_amount": value,
            "runtime_tolerance": 0.0,
            "B_targeting_event_ids": [arrival_id],
            "native_chain_evidence_refs": [
                f"{record_id}-producer",
                departure_id,
                arrival_id,
            ],
            "operational_failure_id": None,
        },
        "window_validity_receipt": {
            "feedback_evaluation_id": f"{record_id}-feedback",
            "feedback_policy_id": "I05-pure-analysis-policy",
            "producer_invocation_id": f"{record_id}-producer",
            "producer_invocation_receipt_sha256": receipt,
            "pre_queue_identity_sha256": _synthetic_sha256(f"pre:{record_id}"),
            "post_queue_identity_sha256": _synthetic_sha256(f"post:{record_id}"),
            "step_processed_event_ids": [departure_id, arrival_id],
            "window_contamination_event_ids": [],
        },
        "arrival_gain_receipt": {
            "native_coherence_domain_id": "I05-synthetic-analysis-domain-[0,1]",
            "native_coherence_domain_lower": 0.0,
            "native_coherence_domain_upper": 1.0,
            "expected_native_arrival_gain": value,
            "arrival_transform_id": "identity_packet_amount_addition",
            "arrival_semantics_source_sha256": ARRIVAL_SOURCE_SHA256,
            "arrival_semantics_receipt_sha256": receipt,
            "arrival_adjustment_event_ids": [],
        },
    }
