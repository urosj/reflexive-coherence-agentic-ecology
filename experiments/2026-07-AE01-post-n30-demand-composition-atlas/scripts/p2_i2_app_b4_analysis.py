"""Pure registry and retained-receipt analysis for P2-I2 APP-B4."""

from __future__ import annotations

from collections import defaultdict
import hashlib
from itertools import product
import json
import math
from typing import Any, Mapping, Sequence

import p2_i2_i04r2_analysis as accepted
from p2_i2_app_b_analysis import _validity as app_b_validity


OPERATIONS = ("G", "E", "P")
SEEDS = (101, 211, 307)
EXCLUDED = ("EEG", "EEE", "EEP")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def feasible_sequences() -> tuple[str, ...]:
    return tuple(
        "".join(symbols)
        for symbols in product(OPERATIONS, repeat=3)
        if "".join(symbols) not in EXCLUDED
    )


def build_registry(freeze: Mapping[str, Any]) -> list[dict[str, Any]]:
    panel = freeze["panel"]
    sequences = feasible_sequences()
    if tuple(panel["seeds"]) != SEEDS:
        raise accepted.ContractError("APP-B4 seeds drifted")
    if tuple(panel["feasible_sequences"]) != sequences:
        raise accepted.ContractError("APP-B4 sequence registry drifted")
    if tuple(panel["excluded_operationally_infeasible_sequences"]) != EXCLUDED:
        raise accepted.ContractError("APP-B4 excluded sequence registry drifted")
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rows.append(
            {
                "arm_id": f"app-b4:history_carried:reference:seed-{seed}",
                "arm_kind": "reference",
                "mode": "history_carried",
                "seed": seed,
                "subset": "reference",
                "sequence": "reference",
                "common_operations": [],
                "history_operations": [],
                "operation_order": ["G", "E", "P"],
                "participant_assignment": "cyclic_A",
                "intervention": "none",
            }
        )
        for sequence in sequences:
            symbols = list(sequence)
            rows.append(
                {
                    "arm_id": f"app-b4:history_carried:{sequence}:seed-{seed}",
                    "arm_kind": "ordered_three_token",
                    "mode": "history_carried",
                    "seed": seed,
                    "subset": sequence,
                    "sequence": sequence,
                    "common_operations": symbols,
                    "history_operations": symbols,
                    "operation_order": symbols,
                    "participant_assignment": "cyclic_A",
                    "intervention": "none",
                }
            )
    if len(rows) != 75:
        raise accepted.ContractError("APP-B4 arm count drifted")
    if panel.get("expanded_registry_digest") and digest_value(rows) != panel["expanded_registry_digest"]:
        raise accepted.ContractError("APP-B4 expanded registry digest drifted")
    return rows


def measurement_payload(envelope: Mapping[str, Any]) -> dict[str, Any]:
    record = envelope["i04r1_response_record"]
    return {
        "status": record["status"],
        "B_before": record["B_before"],
        "B_after": record["B_after"],
        "raw_response": record["raw_response"],
        "oriented_response": record["oriented_response"],
        "carrier_state_digest": record["carrier_state_digest"],
        "pre_packet_queue_length": record["pre_packet_queue_length"],
        "pre_birth_queue_length": record["pre_birth_queue_length"],
        "post_packet_queue_length": record["post_packet_queue_length"],
        "post_birth_queue_length": record["post_birth_queue_length"],
        "feedback_surface_call_count": record["feedback_surface_call_count"],
        "producer_call_count": record["producer_call_count"],
        "step_call_count": record["step_call_count"],
        "step_processed_event_kinds": record["step_processed_event_kinds"],
        "producer_reason": record["producer_reason"],
        "response_packet_id": record["response_packet_id"],
        "departure_event_id": record["departure_event_id"],
        "arrival_event_id": record["arrival_event_id"],
        "response_packet_amount": record["response_packet_amount"],
        "runtime_tolerance": record["runtime_tolerance"],
        "B_targeting_event_ids": record["B_targeting_event_ids"],
        "native_chain_evidence_refs": record["native_chain_evidence_refs"],
        "operational_failure_id": record["operational_failure_id"],
        "window_validity_receipt": envelope["window_validity_receipt"],
        "arrival_gain_receipt": envelope["arrival_gain_receipt"],
    }


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=float(tolerance))


def classify_response_landscape(
    responses_by_seed: Mapping[int, Mapping[str, float]],
    *,
    tolerance: float,
) -> dict[str, Any]:
    sequences = feasible_sequences()
    expected = ("reference", *sequences)
    if tuple(responses_by_seed) != SEEDS:
        raise accepted.ContractError("APP-B4 response seed order drifted")
    for seed in SEEDS:
        if tuple(responses_by_seed[seed]) != expected:
            raise accepted.ContractError("APP-B4 response sequence order drifted")
    seed_invariant = all(
        all(close(responses_by_seed[seed][key], responses_by_seed[SEEDS[0]][key], tolerance) for key in expected)
        for seed in SEEDS[1:]
    )
    exact_total_permutations = ("GEP", "GPE", "EGP", "EPG", "PGE", "PEG")
    groups: dict[str, list[str]] = defaultdict(list)
    for sequence in sequences:
        groups["".join(sorted(sequence))].append(sequence)

    per_seed: dict[int, dict[str, Any]] = {}
    for seed in SEEDS:
        values = responses_by_seed[seed]
        gep = float(values["GEP"])
        responsive = [
            sequence
            for sequence in sequences
            if gep > 0.0 and close(values[sequence], gep, tolerance)
        ]
        nonresponsive = [
            sequence
            for sequence in sequences
            if close(values[sequence], 0.0, tolerance)
        ]
        other = [
            sequence
            for sequence in sequences
            if sequence not in set(responsive) | set(nonresponsive)
        ]
        exact_total_values = {
            sequence: float(values[sequence])
            for sequence in exact_total_permutations
        }
        exact_first = exact_total_values[exact_total_permutations[0]]
        within_multiset = {}
        for multiset, members in sorted(groups.items()):
            member_values = {sequence: float(values[sequence]) for sequence in members}
            first = member_values[members[0]]
            within_multiset[multiset] = {
                "sequences": members,
                "responses": member_values,
                "order_effect": any(
                    not close(value, first, tolerance)
                    for value in member_values.values()
                ),
                "complete_permutation_group": len(members)
                == len(set(__import__("itertools").permutations(multiset))),
            }
        per_seed[seed] = {
            "reference_response": float(values["reference"]),
            "GEP_response": gep,
            "responsive_sequences": responsive,
            "nonresponsive_sequences": nonresponsive,
            "other_response_sequences": other,
            "raw_three_event_cardinality_sufficient": bool(responsive)
            and len(responsive) == len(sequences),
            "raw_three_event_cardinality_excluded_within_feasible_domain": bool(nonresponsive)
            and gep > 0.0,
            "exact_total_permutation_responses": exact_total_values,
            "exact_total_order_effect": any(
                not close(value, exact_first, tolerance)
                for value in exact_total_values.values()
            ),
            "within_multiset_order_effects": within_multiset,
            "GEP_unique_positive_within_feasible_panel": responsive == ["GEP"],
        }

    pattern_fields = (
        "responsive_sequences",
        "nonresponsive_sequences",
        "other_response_sequences",
        "raw_three_event_cardinality_sufficient",
        "raw_three_event_cardinality_excluded_within_feasible_domain",
        "exact_total_order_effect",
        "GEP_unique_positive_within_feasible_panel",
    )
    seed_pattern_invariant = all(
        all(per_seed[seed][field] == per_seed[SEEDS[0]][field] for field in pattern_fields)
        and all(
            per_seed[seed]["within_multiset_order_effects"][multiset]["order_effect"]
            == per_seed[SEEDS[0]]["within_multiset_order_effects"][multiset]["order_effect"]
            for multiset in groups
        )
        for seed in SEEDS[1:]
    )
    canonical = per_seed[SEEDS[0]]
    within_multiset_order_effects = {
        multiset: {
            "sequences": canonical["within_multiset_order_effects"][multiset]["sequences"],
            "responses_by_seed": {
                str(seed): per_seed[seed]["within_multiset_order_effects"][multiset]["responses"]
                for seed in SEEDS
            },
            "order_effect_all_seeds": seed_pattern_invariant
            and all(
                per_seed[seed]["within_multiset_order_effects"][multiset]["order_effect"]
                for seed in SEEDS
            ),
            "complete_permutation_group": canonical["within_multiset_order_effects"][multiset]["complete_permutation_group"],
        }
        for multiset in sorted(groups)
    }
    result = {
        "seed_invariant": seed_invariant,
        "seed_pattern_invariant": seed_pattern_invariant,
        "per_seed": per_seed,
        "responsive_sequences": canonical["responsive_sequences"] if seed_pattern_invariant else [],
        "nonresponsive_sequences": canonical["nonresponsive_sequences"] if seed_pattern_invariant else [],
        "other_response_sequences": canonical["other_response_sequences"] if seed_pattern_invariant else [],
        "raw_three_event_cardinality_sufficient": seed_pattern_invariant
        and all(per_seed[seed]["raw_three_event_cardinality_sufficient"] for seed in SEEDS),
        "raw_three_event_cardinality_excluded_within_feasible_domain": seed_pattern_invariant
        and all(per_seed[seed]["raw_three_event_cardinality_excluded_within_feasible_domain"] for seed in SEEDS),
        "exact_total_permutation_responses_by_seed": {
            str(seed): per_seed[seed]["exact_total_permutation_responses"]
            for seed in SEEDS
        },
        "exact_total_order_effect": seed_pattern_invariant
        and all(per_seed[seed]["exact_total_order_effect"] for seed in SEEDS),
        "within_multiset_order_effects": within_multiset_order_effects,
        "GEP_unique_positive_within_feasible_panel": seed_pattern_invariant
        and all(per_seed[seed]["GEP_unique_positive_within_feasible_panel"] for seed in SEEDS),
        "operation_complementarity_claimed": False,
        "claim_ceiling": "ordered quantitative-history pattern within the unchanged-baseline feasible domain",
    }
    result["classification_digest"] = digest_value(result)
    return result


def analyze_receipts(
    receipts: Sequence[Mapping[str, Any]],
    freeze: Mapping[str, Any],
    machine_policy: Mapping[str, Any],
    parent_policy: Mapping[str, Any],
) -> dict[str, Any]:
    rows = build_registry(freeze)
    expected_ids = [row["arm_id"] for row in rows]
    actual_ids = [str(receipt.get("arm_id")) for receipt in receipts]
    by_id = {str(receipt["arm_id"]): receipt for receipt in receipts}
    row_by_id = {row["arm_id"]: row for row in rows}
    tolerance = float(freeze["response_authority"]["runtime_tolerance"])
    validity: dict[str, Any] = {}
    for arm_id in expected_ids:
        if arm_id not in by_id:
            validity[arm_id] = {"derived_from_receipts": True, "valid": False, "failed_checks": ["missing_arm"], "predicates": []}
            continue
        receipt = by_id[arm_id]
        row = row_by_id[arm_id]
        value = app_b_validity(receipt, row, tolerance, freeze)
        projection = receipt.get("app_b4_measurement_projection", {})
        projection_ok = (
            projection.get("measurement_values_changed") is False
            and projection.get("measurement_payload_digest")
            == digest_value(measurement_payload(receipt["response_envelope"]))
        )
        value["predicates"].append({"check_id": "app_b4_measurement_projection", "passed": projection_ok, "observed": projection})
        if not projection_ok:
            value["failed_checks"].append("app_b4_measurement_projection")
            value["valid"] = False
        validity[arm_id] = value
    matrix_complete = (
        actual_ids == expected_ids
        and len(set(actual_ids)) == 75
        and all(item["valid"] for item in validity.values())
    )
    responses_by_seed: dict[int, dict[str, float]] = {}
    for seed in SEEDS:
        responses_by_seed[seed] = {}
        for sequence in ("reference", *feasible_sequences()):
            arm_id = f"app-b4:history_carried:{sequence}:seed-{seed}"
            receipt = by_id.get(arm_id)
            if receipt is None:
                continue
            accepted.validate_response_envelope(receipt["response_envelope"], machine_policy, parent_policy)
            responses_by_seed[seed][sequence] = float(
                receipt["response_envelope"]["i04r1_response_record"]["oriented_response"]
            )
    classification = None
    if matrix_complete:
        classification = classify_response_landscape(responses_by_seed, tolerance=tolerance)
    result = {
        "analysis_kind": "app_b4_retained_response_landscape",
        "matrix_complete": matrix_complete,
        "arm_count_expected": 75,
        "arm_count_observed": len(receipts),
        "arm_order_exact": actual_ids == expected_ids,
        "all_arms_operationally_valid": all(item["valid"] for item in validity.values()),
        "operational_validity": validity,
        "responses_by_seed": responses_by_seed,
        "classification": classification,
        "excluded_operationally_infeasible_sequences": list(EXCLUDED),
        "excluded_sequences_treated_as_scientific_zero": False,
        "operation_complementarity_claimed": False,
        "scientific_interpretation": None,
    }
    result["analysis_digest"] = digest_value(result)
    return result


__all__ = [
    "EXCLUDED",
    "OPERATIONS",
    "SEEDS",
    "analyze_receipts",
    "build_registry",
    "canonical_bytes",
    "classify_response_landscape",
    "digest_value",
    "feasible_sequences",
    "measurement_payload",
]
