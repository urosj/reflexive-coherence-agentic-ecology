#!/usr/bin/env python3
"""Pure retained-receipt analysis for P2-I2 Appendix B."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

import p2_i2_i04r2_analysis as accepted


MODES = ("state_carried", "history_carried", "hybrid")
SUBSETS = ("reference", "G", "E", "P", "GE", "GP", "EP", "GEP")
PROPER_SUBSETS = SUBSETS[:-1]
SEEDS = (101, 211, 307)


def build_arm_registry(specification: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Expand the frozen compact registry into one exact ordered arm list."""

    if tuple(specification["modes"]) != MODES:
        raise accepted.ContractError("Appendix B mode registry drifted")
    if tuple(specification["subsets"]) != SUBSETS:
        raise accepted.ContractError("Appendix B subset registry drifted")
    if tuple(specification["seeds"]) != SEEDS:
        raise accepted.ContractError("Appendix B seed registry drifted")
    operation_order = tuple(specification["operation_order"])
    if operation_order != ("G", "E", "P"):
        raise accepted.ContractError("Appendix B operation order drifted")
    rows: list[dict[str, Any]] = []
    for mode in MODES:
        for seed in SEEDS:
            for subset in SUBSETS:
                rows.append(
                    {
                        "arm_id": f"primary:{mode}:{subset}:seed-{seed}",
                        "arm_kind": "primary_subset",
                        "mode": mode,
                        "seed": seed,
                        "subset": subset,
                        "common_operations": [] if subset == "reference" else list(subset),
                        "history_operations": []
                        if mode == "state_carried" or subset == "reference"
                        else list(subset),
                        "operation_order": list(operation_order),
                        "participant_assignment": "cyclic_A",
                        "intervention": "none",
                    }
                )
    common_controls = tuple(specification["common_controls"])
    if common_controls != (
        "one_source",
        "rotation_B",
        "rotation_C",
        "label_permutation",
        "private_partition",
        "controller_substitution",
        "carrier_clamp",
    ):
        raise accepted.ContractError("Appendix B common-control registry drifted")
    for mode in MODES:
        for control in common_controls:
            private = control == "private_partition"
            clamp = control == "carrier_clamp"
            rows.append(
                {
                    "arm_id": f"control:{mode}:{control}",
                    "arm_kind": "common_control",
                    "mode": mode,
                    "seed": 101,
                    "subset": "GEP",
                    "common_operations": [] if private else list(operation_order),
                    "history_operations": []
                    if mode == "state_carried" or private or control == "carrier_clamp"
                    else list(operation_order),
                    "operation_order": list(operation_order),
                    "participant_assignment": control
                    if control in {"one_source", "rotation_B", "rotation_C", "label_permutation"}
                    else "cyclic_A",
                    "intervention": control if clamp else "none",
                }
            )
    rows.extend(
        [
            {
                "arm_id": "control:state_carried:equal_C_GPE",
                "arm_kind": "mode_discriminator",
                "mode": "state_carried",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": [],
                "operation_order": ["G", "P", "E"],
                "participant_assignment": "cyclic_A",
                "intervention": "none",
            },
            {
                "arm_id": "control:history_carried:equal_C_GPE",
                "arm_kind": "mode_discriminator",
                "mode": "history_carried",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": list(operation_order),
                "operation_order": ["G", "P", "E"],
                "participant_assignment": "cyclic_A",
                "intervention": "none",
            },
            {
                "arm_id": "control:history_carried:state_only_intervention",
                "arm_kind": "mode_discriminator",
                "mode": "history_carried",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": list(operation_order),
                "operation_order": list(operation_order),
                "participant_assignment": "cyclic_A",
                "intervention": "state_to_reference_after_history",
            },
            {
                "arm_id": "control:hybrid:factorial_ref_C_ref_H",
                "arm_kind": "mode_discriminator",
                "mode": "hybrid",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": [],
                "operation_order": list(operation_order),
                "participant_assignment": "cyclic_A",
                "intervention": "state_and_history_to_reference",
            },
            {
                "arm_id": "control:hybrid:factorial_candidate_C_ref_H",
                "arm_kind": "mode_discriminator",
                "mode": "hybrid",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": [],
                "operation_order": list(operation_order),
                "participant_assignment": "cyclic_A",
                "intervention": "history_to_reference",
            },
            {
                "arm_id": "control:hybrid:factorial_ref_C_candidate_H",
                "arm_kind": "mode_discriminator",
                "mode": "hybrid",
                "seed": 101,
                "subset": "GEP",
                "common_operations": list(operation_order),
                "history_operations": list(operation_order),
                "operation_order": list(operation_order),
                "participant_assignment": "cyclic_A",
                "intervention": "state_to_reference_after_history",
            },
        ]
    )
    if len(rows) != int(specification["expected_arm_count"]):
        raise accepted.ContractError("Appendix B arm count drifted")
    if digest_value(rows) != specification["expanded_registry_digest"]:
        raise accepted.ContractError("Appendix B expanded registry digest drifted")
    return rows


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=float(tolerance))


def strongest_proper_subset_margin(
    envelopes: Mapping[str, Mapping[str, Any]],
    machine_policy: Mapping[str, Any],
    parent_policy: Mapping[str, Any],
    *,
    delta: float,
) -> dict[str, Any]:
    """Extend the accepted estimator to one all-or-none eight-arm tuple."""

    if tuple(envelopes) != SUBSETS:
        raise accepted.ContractError("Appendix B subset order or completeness drifted")
    for envelope in envelopes.values():
        accepted.validate_response_envelope(envelope, machine_policy, parent_policy)
    records = {key: value["i04r1_response_record"] for key, value in envelopes.items()}
    pairing_fields = (
        "mode",
        "seed",
        "physical_order_id",
        "pairing_identity",
        "opportunity_id",
        "window_protocol_id",
        "B_before",
        "response_id",
        "unit",
    )
    candidate = records["GEP"]
    drift = [
        field
        for field in pairing_fields
        if any(record[field] != candidate[field] for record in records.values())
    ]
    if drift:
        raise accepted.ContractError(f"Appendix B pairing drift: {drift}")
    for subset, record in records.items():
        if record["branch_id"] != subset:
            raise accepted.ContractError("Appendix B branch/subset identity drifted")
    invalid = [
        subset
        for subset, record in records.items()
        if record["status"] not in accepted.SCIENTIFIC_STATUSES
    ]
    selected_subset: str | None = None
    strongest: float | None = None
    margin: float | None = None
    if not invalid:
        selected_subset = PROPER_SUBSETS[0]
        strongest = float(records[selected_subset]["oriented_response"])
        for subset in PROPER_SUBSETS[1:]:
            value = float(records[subset]["oriented_response"])
            if value > strongest:
                strongest = value
                selected_subset = subset
        margin = accepted.base.normalized_paired_difference(
            float(candidate["oriented_response"]),
            strongest,
            float(parent_policy["paired_margin"]["analysis_arithmetic_floor"]),
        )
    return {
        "mode": candidate["mode"],
        "seed": candidate["seed"],
        "physical_order_id": candidate["physical_order_id"],
        "pairing_identity": candidate["pairing_identity"],
        "candidate_record_id": candidate["record_id"],
        "proper_subset_record_ids": {
            subset: records[subset]["record_id"] for subset in PROPER_SUBSETS
        },
        "responses": {subset: records[subset]["oriented_response"] for subset in SUBSETS},
        "selected_comparator_subset": selected_subset,
        "strongest_proper_subset_response": strongest,
        "complete_eight_arm_tuple_valid": not invalid,
        "nonevaluable_subsets": invalid,
        "normalized_margin": margin,
        "analysis_arithmetic_delta": float(delta),
        "primary_passed": margin is not None and margin > float(delta),
        "estimator_path_id": "p2-i2-app-b-accepted-normalized-eight-arm-extension-v1",
    }


def _validity(
    receipt: Mapping[str, Any],
    row: Mapping[str, Any],
    tolerance: float,
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    predicates: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, observed: Any = None) -> None:
        predicates.append({"check_id": check_id, "passed": bool(passed), "observed": observed})

    add("arm_id", receipt.get("arm_id") == row.get("arm_id"), receipt.get("arm_id"))
    add("row_digest", receipt.get("arm_row_digest") == digest_value(row), receipt.get("arm_row_digest"))
    process = receipt.get("process_receipt", {})
    add("fresh_process", process.get("fresh_process") is True, process)
    add("repository_venv", process.get("logical_executable") == ".venv/bin/python", process)
    add("checkout_pygrc", process.get("pygrc_source") == "external-repository:graph-reflexive-coherence/src", process)
    baseline = receipt.get("baseline", {})
    add("fresh_model", baseline.get("fresh_model") is True, baseline)
    add("accepted_topology", baseline.get("node_count") == 23 and baseline.get("edge_count") == 16, baseline)
    operations = receipt.get("operation_receipts", [])
    add("three_slots", len(operations) == 3, len(operations))
    add("operation_order", [item.get("operation") for item in operations] == list(row.get("operation_order", [])), operations)
    operation_registry = freeze["operation_registry"]
    schedule = freeze["schedule"]
    private = str(row.get("arm_id", "")).endswith(":private_partition")
    for index, operation in enumerate(operations):
        operation_id = str(operation.get("operation"))
        selected = operation_id in set(row.get("common_operations", []))
        registered = operation_registry[operation_id]
        if selected:
            expected_route = registered["common_route"]
        elif private and operation_id in {"G", "P"}:
            expected_route = registered["private_route"]
        elif operation_id == "E":
            expected_route = registered["diversion_and_private_matched_route"]
        else:
            expected_route = registered["diversion_route"]
        add(f"operation_{index}_selection", operation.get("selected_common") is selected, operation)
        add(
            f"operation_{index}_route",
            [operation.get("source_role"), operation.get("target_role"), operation.get("edge_role")]
            == expected_route,
            [operation.get("source_role"), operation.get("target_role"), operation.get("edge_role")],
        )
        add(
            f"operation_{index}_amount",
            close(operation.get("amount", -1.0), registered["amount"], tolerance),
            operation.get("amount"),
        )
        steps = operation.get("steps", [])
        bookkeeping = [step.get("bookkeeping", {}) for step in steps]
        processed_kinds = [item.get("processed_event_kind") for item in bookkeeping]
        processed_ids = [item.get("processed_event_id") for item in bookkeeping]
        add(
            f"operation_{index}_native_steps",
            len(steps) == 2
            and processed_kinds == ["lgrc9v3_packet_departure", "lgrc9v3_packet_arrival"]
            and all(isinstance(item, str) and item for item in processed_ids)
            and len(set(processed_ids)) == 2,
            {"processed_kinds": processed_kinds, "processed_ids": processed_ids},
        )
        add(
            f"operation_{index}_native_timing",
            len(bookkeeping) == 2
            and close(bookkeeping[0].get("event_time_key", -1.0), schedule["operation_departures"][index], tolerance)
            and close(bookkeeping[1].get("event_time_key", -1.0), schedule["operation_arrivals"][index], tolerance)
            and bookkeeping[0].get("queue_length_after") == 1
            and bookkeeping[1].get("queue_length_after") == 0,
            bookkeeping,
        )
        add(f"operation_{index}_budget", abs(float(operation.get("max_abs_budget_error", math.inf))) <= tolerance, operation.get("max_abs_budget_error"))
    history = receipt.get("history_receipt", {})
    expected_tokens = len(row.get("history_operations", [])) if row.get("mode") != "state_carried" else 0
    add("history_token_count", len(history.get("tokens", [])) == expected_tokens, history)
    add("history_source_label_free", all("actor" not in token and "source_label" not in token for token in history.get("tokens", [])), history)
    expected_admissions = (
        []
        if row.get("mode") == "state_carried"
        else [
            operation
            for operation in row.get("operation_order", [])
            if operation in set(row.get("common_operations", []))
        ]
    )
    observed_admissions = [
        item.get("physical_operation")
        for item in history.get("physical_admission_receipts", [])
    ]
    add("history_physical_admissions", observed_admissions == expected_admissions, observed_admissions)
    response = receipt.get("response_receipt", {})
    add("window_valid", response.get("window_valid") is True, response)
    add("gain_matches", response.get("gain_matches") is True, response)
    add("queue_empty", response.get("queue_empty_after") is True, response)
    envelope = receipt.get("response_envelope", {})
    add("envelope_present", set(envelope) == {"i04r1_response_record", "window_validity_receipt", "arrival_gain_receipt"}, sorted(envelope))
    restoration = receipt.get("restoration_receipt", {})
    add("load_identity", restoration.get("identity_before_save") == restoration.get("identity_after_load"), restoration)
    add("reset_identity", restoration.get("identity_after_reset") == baseline.get("identity"), restoration)
    resource = receipt.get("resource_receipt", {})
    add("resource_nodes", resource.get("node_count") == 23, resource)
    add("resource_edges", resource.get("edge_count") == 16, resource)
    add("resource_queue", int(resource.get("maximum_queue_length", 10**9)) <= 1, resource)
    failed = [item["check_id"] for item in predicates if not item["passed"]]
    return {
        "derived_from_receipts": True,
        "valid": not failed,
        "failed_checks": failed,
        "predicate_count": len(predicates),
        "predicates": predicates,
    }


def _response(receipt: Mapping[str, Any]) -> float:
    return float(receipt["response_envelope"]["i04r1_response_record"]["oriented_response"])


def analyze_receipts(
    receipts: Sequence[Mapping[str, Any]],
    freeze: Mapping[str, Any],
    machine_policy: Mapping[str, Any],
    parent_policy: Mapping[str, Any],
) -> dict[str, Any]:
    rows = build_arm_registry(freeze["arm_registry_specification"])
    expected_ids = [row["arm_id"] for row in rows]
    actual_ids = [receipt.get("arm_id") for receipt in receipts]
    by_id = {str(receipt["arm_id"]): receipt for receipt in receipts}
    row_by_id = {str(row["arm_id"]): row for row in rows}
    tolerance = float(freeze["response_authority"]["runtime_tolerance"])
    validity = {
        arm_id: _validity(by_id[arm_id], row_by_id[arm_id], tolerance, freeze)
        if arm_id in by_id
        else {"derived_from_receipts": True, "valid": False, "failed_checks": ["missing_arm"], "predicate_count": 1, "predicates": []}
        for arm_id in expected_ids
    }
    matrix_complete = (
        actual_ids == expected_ids
        and len(set(actual_ids)) == len(expected_ids)
        and all(item["valid"] for item in validity.values())
    )
    delta = float(freeze["response_authority"]["analysis_arithmetic_delta"])
    primary: dict[str, list[dict[str, Any]]] = {mode: [] for mode in MODES}
    for mode in MODES:
        for seed in SEEDS:
            envelopes = {
                subset: by_id[f"primary:{mode}:{subset}:seed-{seed}"]["response_envelope"]
                for subset in SUBSETS
                if f"primary:{mode}:{subset}:seed-{seed}" in by_id
            }
            if tuple(envelopes) == SUBSETS:
                primary[mode].append(
                    strongest_proper_subset_margin(
                        envelopes,
                        machine_policy,
                        parent_policy,
                        delta=delta,
                    )
                )

    controls: dict[str, Any] = {}
    mode_dispositions: dict[str, Any] = {}
    for mode in MODES:
        gep = by_id.get(f"primary:{mode}:GEP:seed-101")
        subset = {
            name: by_id.get(f"primary:{mode}:{name}:seed-101") for name in SUBSETS
        }
        operation_necessity = {
            "G": gep is not None and subset["EP"] is not None and not close(_response(gep), _response(subset["EP"]), tolerance),
            "E": gep is not None and subset["GP"] is not None and not close(_response(gep), _response(subset["GP"]), tolerance),
            "P": gep is not None and subset["GE"] is not None and not close(_response(gep), _response(subset["GE"]), tolerance),
        }
        clamp = by_id.get(f"control:{mode}:carrier_clamp")
        private = by_id.get(f"control:{mode}:private_partition")
        controller = by_id.get(f"control:{mode}:controller_substitution")
        identity_controls = {
            "one_source": by_id.get(f"control:{mode}:one_source"),
            "rotation_B": by_id.get(f"control:{mode}:rotation_B"),
            "rotation_C": by_id.get(f"control:{mode}:rotation_C"),
            "label_permutation": by_id.get(f"control:{mode}:label_permutation"),
        }
        identity_pass = gep is not None and all(
            item is not None
            and close(_response(item), _response(gep), tolerance)
            and close(item["response_receipt"]["boundary_score"], gep["response_receipt"]["boundary_score"], tolerance)
            for item in identity_controls.values()
        )
        common = {
            "operation_necessity": operation_necessity,
            "carrier_clamp_changes_response": gep is not None and clamp is not None and not close(_response(gep), _response(clamp), tolerance),
            "private_partition_does_not_reproduce": private is not None and close(_response(private), 0.0, tolerance),
            "controller_substitution_excluded": controller is not None and controller["response_receipt"].get("controller_authored") is True,
            "identity_controls_reproduce": identity_pass,
            "participant_plurality_non_load_bearing": identity_pass,
        }
        if mode == "state_carried":
            order = by_id.get("control:state_carried:equal_C_GPE")
            discriminator = {
                "equal_final_C": gep is not None and order is not None and close(gep["carrier_receipt"]["P_after"], order["carrier_receipt"]["P_after"], tolerance),
                "equal_response": gep is not None and order is not None and close(_response(gep), _response(order), tolerance),
            }
        elif mode == "history_carried":
            order = by_id.get("control:history_carried:equal_C_GPE")
            state_only = by_id.get("control:history_carried:state_only_intervention")
            discriminator = {
                "equal_final_C": gep is not None and order is not None and close(gep["carrier_receipt"]["P_after"], order["carrier_receipt"]["P_after"], tolerance),
                "different_history": gep is not None and order is not None and gep["history_receipt"]["token_digest"] != order["history_receipt"]["token_digest"],
                "different_response": gep is not None and order is not None and not close(_response(gep), _response(order), tolerance),
                "state_only_intervention_inert": gep is not None and state_only is not None and not close(gep["carrier_receipt"]["P_after"], state_only["carrier_receipt"]["P_after"], tolerance) and close(_response(gep), _response(state_only), tolerance),
            }
        else:
            rr = by_id.get("control:hybrid:factorial_ref_C_ref_H")
            cr = by_id.get("control:hybrid:factorial_candidate_C_ref_H")
            rc = by_id.get("control:hybrid:factorial_ref_C_candidate_H")
            discriminator = {
                "reference_zero": rr is not None and close(_response(rr), 0.0, tolerance),
                "state_only_zero": cr is not None and close(_response(cr), 0.0, tolerance),
                "history_only_zero": rc is not None and close(_response(rc), 0.0, tolerance),
                "full_positive": gep is not None and _response(gep) > 0.0,
                "both_components_affect_same_response": rr is not None and cr is not None and rc is not None and gep is not None and close(_response(rr), _response(cr), tolerance) and close(_response(rr), _response(rc), tolerance) and not close(_response(rr), _response(gep), tolerance),
            }
        margins = primary[mode]
        primary_complete = len(margins) == len(SEEDS) and all(item["complete_eight_arm_tuple_valid"] for item in margins)
        primary_pass = primary_complete and all(item["primary_passed"] for item in margins)
        causal_pass = all(operation_necessity.values()) and common["carrier_clamp_changes_response"]
        discriminator_pass = all(discriminator.values())
        controls[mode] = {"common": common, "discriminator": discriminator}
        supported = matrix_complete and primary_pass and causal_pass and discriminator_pass and common["private_partition_does_not_reproduce"] and identity_pass
        mode_dispositions[mode] = {
            "primary_complete": primary_complete,
            "primary_passed": primary_pass,
            "causal_requirements_passed": causal_pass,
            "carrier_and_identity_controls_passed": common["private_partition_does_not_reproduce"] and identity_pass,
            "mode_discriminator_passed": discriminator_pass,
            "supported": supported,
            "classification": "supported_bounded_composition" if supported else "not_supported_in_frozen_realization",
        }

    supported_modes = [mode for mode in MODES if mode_dispositions[mode]["supported"]]
    terminal = "supported_bounded_candidate" if supported_modes else "not_supported_in_frozen_realizations"
    result = {
        "analysis_kind": "retained_receipt_projection",
        "matrix_complete": matrix_complete,
        "arm_count_expected": len(expected_ids),
        "arm_count_observed": len(receipts),
        "arm_order_exact": actual_ids == expected_ids,
        "all_arms_operationally_valid": all(item["valid"] for item in validity.values()),
        "operational_validity": validity,
        "primary_results": primary,
        "controls": controls,
        "mode_dispositions": mode_dispositions,
        "supported_modes": supported_modes,
        "terminal_classification": terminal,
        "bounded_claim": "bounded P2-I2-grounded three-operation shared-pool composition candidate" if supported_modes else None,
        "cross_appendix_recurrence_claimed": False,
        "blocked_claims": list(freeze["claim_ceiling"]["blocked_claims"]),
    }
    result["analysis_digest"] = digest_value(result)
    return result


__all__ = [
    "MODES",
    "PROPER_SUBSETS",
    "SEEDS",
    "SUBSETS",
    "analyze_receipts",
    "build_arm_registry",
    "canonical_bytes",
    "digest_value",
    "strongest_proper_subset_margin",
]
