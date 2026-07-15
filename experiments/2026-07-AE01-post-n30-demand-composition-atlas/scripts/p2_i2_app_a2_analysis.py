#!/usr/bin/env python3
"""Pure retained-receipt analysis for P2-I2 APP-A2.

This module intentionally imports no PyGRC surface.  Both the campaign parent
and the read-only reconstructor use the same deterministic projection.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


AXES = ("environment", "support", "distinguishability", "boundary")
PRIMARY_SUBSETS = ("reference", "G", "E", "P", "GE", "GP", "EP")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=tolerance)


def vector_delta(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, float]:
    return {axis: float(left[axis]) - float(right[axis]) for axis in AXES}


def vector_changed(left: Mapping[str, Any], right: Mapping[str, Any], tolerance: float) -> bool:
    return any(not close(float(left[axis]), float(right[axis]), tolerance) for axis in AXES)


def derive_operational_validity(
    receipt: Mapping[str, Any],
    arm_row: Mapping[str, Any],
    *,
    tolerance: float,
    retention_fraction: float,
    intervention_targets: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive arm validity only from retained public-call/runtime receipts."""

    predicates: list[dict[str, Any]] = []

    def add(predicate_id: str, passed: bool, observed: Any = None) -> None:
        predicates.append(
            {
                "predicate_id": predicate_id,
                "passed": bool(passed),
                "observed": observed,
            }
        )

    add("arm_id", receipt.get("arm_id") == arm_row.get("arm_id"), receipt.get("arm_id"))
    add("arm_row_digest", receipt.get("arm_row_digest") == digest_value(arm_row), receipt.get("arm_row_digest"))
    process = receipt.get("process_receipt", {})
    add("fresh_process_contract", process.get("fresh_child_process") is True, process)
    add("repository_venv", process.get("logical_executable") == ".venv/bin/python", process.get("logical_executable"))
    add("checkout_pygrc", process.get("pygrc_identity") == {"repository_id": "graph-reflexive-coherence", "path": "src/pygrc/__init__.py"}, process.get("pygrc_identity"))

    baseline = receipt.get("baseline", {})
    add("fresh_model", baseline.get("fresh_model") is True, baseline.get("fresh_model"))
    add("topology_nodes", baseline.get("node_count") == 12, baseline.get("node_count"))
    add("topology_edges", baseline.get("edge_count") == 28, baseline.get("edge_count"))
    role_node_ids = baseline.get("role_node_ids", {})
    edge_role_ids = baseline.get("edge_role_ids", {})
    add("role_node_registry", len(role_node_ids) == 12, role_node_ids)
    add("edge_role_registry", len(edge_role_ids) == 28, edge_role_ids)

    operations = receipt.get("operation_receipts", [])
    expected_sequence = list(arm_row.get("sequence", []))
    add("three_operation_slots", len(operations) == 3, len(operations))
    add("frozen_sequence", [row.get("operation") for row in operations] == expected_sequence, [row.get("operation") for row in operations])
    continuity = baseline.get("identity")
    common_operations = set(arm_row.get("common_operations", []))
    for position, operation in enumerate(operations):
        operation_id = str(operation.get("operation"))
        selected = operation_id in common_operations
        add(f"op{position}.position", operation.get("position") == position, operation.get("position"))
        add(f"op{position}.selection", operation.get("selected_common") is selected, operation.get("selected_common"))
        add(f"op{position}.namespace", operation.get("route_namespace") == ("common" if selected else "diversion"), operation.get("route_namespace"))
        add(f"op{position}.input_identity", operation.get("input_identity") == continuity, operation.get("input_identity"))
        transfers = operation.get("transfers", [])
        add(f"op{position}.four_packets", len(transfers) == 4, len(transfers))
        add(f"op{position}.cost_proxy", close(operation.get("cost_proxy", -1.0), sum(float(row.get("amount", 0.0)) for row in transfers), tolerance), operation.get("cost_proxy"))
        for transfer_index, transfer in enumerate(transfers):
            events = transfer.get("processed_events", [])
            add(
                f"op{position}.packet{transfer_index}.event_pair",
                [row.get("event_kind") for row in events]
                == ["lgrc9v3_packet_departure", "lgrc9v3_packet_arrival"],
                [row.get("event_kind") for row in events],
            )
            amount = float(transfer.get("amount", 0.0))
            add(f"op{position}.packet{transfer_index}.source_delta", close(transfer.get("source_delta", 0.0), -amount, tolerance), transfer.get("source_delta"))
            add(f"op{position}.packet{transfer_index}.target_delta", close(transfer.get("target_delta", 0.0), amount, tolerance), transfer.get("target_delta"))
            add(f"op{position}.packet{transfer_index}.budget", all(abs(float(row.get("budget_error", 0.0))) <= tolerance for row in events), [row.get("budget_error") for row in events])
            packet = transfer.get("packet_record", {})
            source_role = transfer.get("source_role")
            target_role = transfer.get("target_role")
            edge_role = transfer.get("edge_role")
            add(f"op{position}.packet{transfer_index}.record_amount", close(packet.get("amount", -1.0), amount, tolerance), packet.get("amount"))
            add(f"op{position}.packet{transfer_index}.record_source", packet.get("source_node_id") == role_node_ids.get(source_role), packet.get("source_node_id"))
            add(f"op{position}.packet{transfer_index}.record_target", packet.get("target_node_id") == role_node_ids.get(target_role), packet.get("target_node_id"))
            add(f"op{position}.packet{transfer_index}.record_edge", packet.get("edge_id") == edge_role_ids.get(edge_role), packet.get("edge_id"))
            add(f"op{position}.packet{transfer_index}.record_arrived", packet.get("packet_state") == "arrived", packet.get("packet_state"))
        continuity = operation.get("output_identity")

    pre_intervention = receipt.get("pre_intervention", {})
    add("pre_intervention_continuity", pre_intervention.get("identity") == continuity, pre_intervention.get("identity"))
    intervention = receipt.get("intervention")
    if arm_row.get("intervention") == "none":
        add("no_intervention", intervention is None, intervention)
        expected_pre_r_identity = pre_intervention.get("identity")
    else:
        add("intervention_present", isinstance(intervention, Mapping), intervention)
        if isinstance(intervention, Mapping):
            rebase = intervention.get("packet_ledger_rebase", {})
            add("intervention_before_identity", intervention.get("identity_before") == pre_intervention.get("identity"), intervention.get("identity_before"))
            add("intervention_public_set_state", intervention.get("state_setter") == "public LGRC9V3.set_state", intervention.get("state_setter"))
            add("intervention_history_preserved", rebase.get("packet_history_preserved") is True and rebase.get("packet_event_history_preserved") is True, rebase)
            add("intervention_empty_queue", rebase.get("queue_was_empty") is True, rebase.get("queue_was_empty"))
            add("intervention_budget", abs(float(rebase.get("new_budget_error", math.inf))) <= tolerance, rebase.get("new_budget_error"))
            registered_target_key = (
                "matched_reference_pre_r"
                if arm_row.get("intervention")
                == "clamp_all_carrier_axes_to_matched_reference_pre_r"
                else "registered_GEP_pre_r"
            )
            registered_target = intervention_targets.get(registered_target_key, {})
            target_carrier = intervention.get("target_carrier", {})
            after_carrier = intervention.get("after_carrier", {})
            add("intervention_registered_target", all(close(target_carrier.get(axis, math.inf), registered_target.get(axis, -math.inf), tolerance) for axis in AXES), target_carrier)
            add("intervention_target_realized", all(close(after_carrier.get(axis, math.inf), target_carrier.get(axis, -math.inf), tolerance) for axis in AXES), after_carrier)
            add("intervention_target_total", close(intervention.get("target_carrier_total", math.inf), sum(float(target_carrier.get(axis, math.inf)) for axis in AXES), tolerance), intervention.get("target_carrier_total"))
            expected_pre_r_identity = intervention.get("identity_after")
        else:
            expected_pre_r_identity = None

    pre_r = receipt.get("pre_r", {})
    add("pre_r_identity", pre_r.get("identity") == expected_pre_r_identity, pre_r.get("identity"))
    response = receipt.get("response", {})
    add("response_input_identity", response.get("input_identity") == pre_r.get("identity"), response.get("input_identity"))
    add("response_four_packets", len(response.get("packet_records", [])) == 4, len(response.get("packet_records", [])))
    add("response_eight_events", len(response.get("processed_events", [])) == 8, len(response.get("processed_events", [])))
    event_kinds = [row.get("event_kind") for row in response.get("processed_events", [])]
    add("response_event_kinds", event_kinds.count("lgrc9v3_packet_departure") == 4 and event_kinds.count("lgrc9v3_packet_arrival") == 4, event_kinds)
    producer_records = response.get("producer_records", [])
    add("response_native_producer_records", len(producer_records) == 4 and all(row.get("reason_code") == "packet_departure_scheduled" and row.get("scheduled_event_kind") == "lgrc9v3_packet_departure" for row in producer_records), producer_records)
    add("response_carrier_sources_only", set(response.get("source_roles", [])) == {f"c_{axis}" for axis in AXES}, response.get("source_roles"))
    add("response_targets_r_only", set(response.get("target_roles", [])) == {"r"}, response.get("target_roles"))
    response_packets = response.get("packet_records", [])
    add("response_packet_routes", all(packet.get("source_node_id") in {role_node_ids.get(f"c_{axis}") for axis in AXES} and packet.get("target_node_id") == role_node_ids.get("r") and packet.get("packet_state") == "arrived" for packet in response_packets), response_packets)
    add("response_queue_empty", response.get("queue_empty_after") is True, response.get("queue_empty_after"))
    add("response_fraction", close(response.get("retention_fraction", -1.0), retention_fraction, tolerance), response.get("retention_fraction"))
    add("response_mass_axes", set(response.get("packet_mass_by_axis", {})) == set(AXES), sorted(response.get("packet_mass_by_axis", {})))
    add("unregistered_mass_zero", abs(float(response.get("unregistered_shared_carrier_packet_mass", math.inf))) <= tolerance, response.get("unregistered_shared_carrier_packet_mass"))

    resource = receipt.get("resource_receipt", {})
    add("resource_packet_events", int(resource.get("packet_events", 10**9)) <= 32, resource.get("packet_events"))
    add("resource_queue", int(resource.get("maximum_queue_length", 10**9)) <= 4, resource.get("maximum_queue_length"))
    add("resource_nodes", resource.get("node_count") == 12, resource.get("node_count"))
    add("resource_edges", resource.get("edge_count") == 28, resource.get("edge_count"))

    restoration = receipt.get("restoration", {})
    add("save_load_identity", restoration.get("identity_before_save") == restoration.get("identity_after_load"), restoration)
    add("empty_step_continuation", restoration.get("original_after_empty_step") == restoration.get("loaded_after_empty_step"), restoration)
    add("original_reset", restoration.get("original_after_reset") == baseline.get("identity"), restoration.get("original_after_reset"))
    add("loaded_reset", restoration.get("loaded_after_reset") == baseline.get("identity"), restoration.get("loaded_after_reset"))

    failed = [row["predicate_id"] for row in predicates if not row["passed"]]
    return {
        "derived_from_receipts": True,
        "valid": not failed,
        "predicate_count": len(predicates),
        "failed_predicates": failed,
        "predicates": predicates,
    }


def derive_gate_signature(
    receipt: Mapping[str, Any],
    reference: Mapping[str, Any],
    *,
    gates: Mapping[str, Any],
    tolerance: float,
    retention_fraction: float,
) -> dict[str, Any]:
    response = receipt["response"]
    reference_response = reference["response"]
    response_delta = vector_delta(response["packet_mass_by_axis"], reference_response["packet_mass_by_axis"])
    carrier_delta = vector_delta(receipt["pre_r"]["carrier"], reference["pre_r"]["carrier"])
    residual_by_axis = {
        axis: abs(carrier_delta[axis] - response_delta[axis]) for axis in AXES
    }
    phase_residual = max(residual_by_axis.values())
    leakage = (
        float(response["unregistered_shared_carrier_packet_mass"])
        + abs(float(response["max_abs_native_budget_error"]))
    ) / max(1.0, float(response["total_registered_common_carrier_packet_mass"]))
    environment_pass = response_delta["environment"] + tolerance >= float(gates["environment_feedback"]["threshold"])
    support_pass = response_delta["support"] + tolerance >= float(gates["support_feedback"]["threshold"])
    phase_pass = phase_residual <= float(gates["phase_residual"]["threshold"]) + tolerance
    leakage_pass = leakage <= float(gates["registered_route_merge_leakage"]["threshold"]) + tolerance
    measured = {
        "environment_feedback": {
            "value": response_delta["environment"],
            "passed": environment_pass,
        },
        "support_feedback": {
            "value": response_delta["support"],
            "passed": support_pass,
        },
        "phase_residual": {
            "value": phase_residual,
            "by_axis": residual_by_axis,
            "passed": phase_pass,
        },
        "registered_route_merge_leakage": {
            "value": leakage,
            "passed": leakage_pass,
        },
    }
    return {
        "matched_reference": receipt["arm_row"]["matched_reference"],
        "configuration_retention_fraction": float(response["retention_fraction"]),
        "configuration_condition_passed": close(response["retention_fraction"], retention_fraction, tolerance),
        "carrier_delta_by_axis": carrier_delta,
        "response_delta_by_axis": response_delta,
        "measured_gates": measured,
        "all_measured_gates_passed": all(row["passed"] for row in measured.values()),
    }


def analyze_receipts(
    receipts: Sequence[Mapping[str, Any]],
    fixture_freeze: Mapping[str, Any],
    execution_freeze: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive the complete APP-A2 result from retained receipts only."""

    tolerance = float(fixture_freeze["measurement_authority"]["runtime_tolerance"])
    retention_fraction = float(fixture_freeze["measurement_authority"]["retention_fraction"])
    frozen_rows = fixture_freeze["arm_registry"]
    expected_ids = execution_freeze["frozen_registry_import"]["arm_order"]
    actual_ids = [row.get("arm_id") for row in receipts]
    unique = len(set(actual_ids)) == len(actual_ids)
    order_exact = actual_ids == expected_ids
    by_id = {str(row["arm_id"]): row for row in receipts}

    validity: dict[str, Any] = {}
    for arm_row in frozen_rows:
        arm_id = str(arm_row["arm_id"])
        if arm_id in by_id:
            validity[arm_id] = derive_operational_validity(
                by_id[arm_id],
                arm_row,
                tolerance=tolerance,
                retention_fraction=retention_fraction,
                intervention_targets=execution_freeze["frozen_registry_import"]["registered_intervention_targets"],
            )
        else:
            validity[arm_id] = {
                "derived_from_receipts": True,
                "valid": False,
                "predicate_count": 1,
                "failed_predicates": ["missing_arm"],
                "predicates": [
                    {
                        "predicate_id": "missing_arm",
                        "passed": False,
                        "observed": None,
                    }
                ],
            }

    signatures: dict[str, Any] = {}
    for arm_row in frozen_rows:
        arm_id = str(arm_row["arm_id"])
        reference_id = str(arm_row["matched_reference"])
        if arm_id not in by_id:
            continue
        if reference_id == "self":
            reference_id = arm_id
        if reference_id not in by_id:
            continue
        signatures[arm_id] = derive_gate_signature(
            by_id[arm_id],
            by_id[reference_id],
            gates=fixture_freeze["measurement_authority"]["gates"],
            tolerance=tolerance,
            retention_fraction=retention_fraction,
        )

    all_valid = all(validity[arm_id]["valid"] for arm_id in expected_ids)
    all_signatures = set(signatures) == set(expected_ids)
    matrix_complete = (
        len(receipts) == len(expected_ids)
        and unique
        and order_exact
        and all_valid
        and all_signatures
    )

    proper_subset_failures = {
        arm_id: (
            arm_id in signatures
            and signatures[arm_id]["configuration_condition_passed"]
            and not signatures[arm_id]["all_measured_gates_passed"]
        )
        for arm_id in PRIMARY_SUBSETS
    }
    primary_relation = (
        matrix_complete
        and signatures["GEP"]["configuration_condition_passed"]
        and signatures["GEP"]["all_measured_gates_passed"]
        and all(proper_subset_failures.values())
    )

    withdrawal_map = {"G": "EP", "E": "GP", "P": "GE"}
    restore_map = {
        "G": "mediator_restore_G",
        "E": "mediator_restore_E",
        "P": "mediator_restore_P",
    }
    operation_causality: dict[str, Any] = {}
    for operation in ("G", "E", "P"):
        withdrawal = withdrawal_map[operation]
        restore = restore_map[operation]
        direct_changed = (
            matrix_complete
            and vector_changed(
                by_id["GEP"]["response"]["packet_mass_by_axis"],
                by_id[withdrawal]["response"]["packet_mass_by_axis"],
                tolerance,
            )
        )
        mediator_changed = (
            matrix_complete
            and vector_changed(
                by_id[restore]["response"]["packet_mass_by_axis"],
                by_id[withdrawal]["response"]["packet_mass_by_axis"],
                tolerance,
            )
        )
        operation_causality[operation] = {
            "withdrawal_arm": withdrawal,
            "mediator_restore_arm": restore,
            "direct_response_changed": direct_changed,
            "mediator_intervention_changed_response": mediator_changed,
            "causal_requirement_passed": direct_changed or mediator_changed,
        }
    clamp_changed = (
        matrix_complete
        and vector_changed(
            by_id["GEP"]["response"]["packet_mass_by_axis"],
            by_id["carrier_clamp_GEP"]["response"]["packet_mass_by_axis"],
            tolerance,
        )
    )
    causal_relation = (
        matrix_complete
        and all(row["causal_requirement_passed"] for row in operation_causality.values())
        and clamp_changed
    )

    one_source_reproduces = (
        matrix_complete and signatures["one_source_GEP"]["all_measured_gates_passed"]
    )
    rotation_reproduces = (
        matrix_complete and signatures["cyclic_rotation_GEP"]["all_measured_gates_passed"]
    )
    primary_response_delta = signatures.get("GEP", {}).get("response_delta_by_axis", {})
    label_response_delta = signatures.get("label_permuted_GEP", {}).get("response_delta_by_axis", {})
    label_invariant = (
        matrix_complete
        and all(close(primary_response_delta[axis], label_response_delta[axis], tolerance) for axis in AXES)
    )
    order_passes = {
        arm_id: matrix_complete and signatures[arm_id]["all_measured_gates_passed"]
        for arm_id in ("order_EGP", "order_GPE")
    }
    order_losses = [arm_id for arm_id, passed in order_passes.items() if not passed]
    if len(order_losses) == 2:
        order_resolution = "bounded_G_then_E_then_P_sequence_load_bearing"
    elif len(order_losses) == 1:
        order_resolution = "at_least_one_source_grounded_handoff_order_sensitive"
    else:
        order_resolution = "tested_adjacent_inversions_do_not_make_order_load_bearing"

    if not matrix_complete:
        terminal = "nonevaluable_incomplete_or_invalid_matrix"
    elif primary_relation and causal_relation:
        terminal = "supported_bounded_candidate"
    else:
        terminal = "not_supported_in_frozen_fixture"

    if one_source_reproduces:
        plurality = "physical_participant_plurality_non_load_bearing_in_frozen_fixture"
    elif rotation_reproduces:
        plurality = "bounded_plurality_candidate_requires_matched_conditions"
    else:
        plurality = "participant_plurality_unresolved"

    result = {
        "analysis_kind": "read_only_receipt_projection",
        "arm_count_expected": len(expected_ids),
        "arm_count_observed": len(receipts),
        "arm_ids_unique": unique,
        "arm_order_exact": order_exact,
        "all_arms_operationally_valid": all_valid,
        "all_gate_signatures_derived": all_signatures,
        "matrix_complete": matrix_complete,
        "operational_validity": validity,
        "gate_signatures": signatures,
        "proper_subset_failures": proper_subset_failures,
        "primary_relation_passed": primary_relation,
        "operation_causality": operation_causality,
        "carrier_clamp_changed_response": clamp_changed,
        "causal_relation_passed": causal_relation,
        "controls": {
            "one_source_reproduces": one_source_reproduces,
            "cyclic_role_rotation_reproduces": rotation_reproduces,
            "label_permutation_invariant": label_invariant,
            "order_inversion_gate_passes": order_passes,
            "order_resolution": order_resolution,
            "reference_all_diverted": (
                matrix_complete
                and all(not row["selected_common"] for row in by_id["reference"]["operation_receipts"])
            ),
            "response_sources_carrier_only": (
                matrix_complete
                and all(
                    set(receipt["response"]["source_roles"])
                    == {f"c_{axis}" for axis in AXES}
                    for receipt in receipts
                )
            ),
        },
        "terminal_classification": terminal,
        "bounded_claim": (
            execution_freeze["interpretation_contract"]["positive_primary_ceiling"]
            if terminal == "supported_bounded_candidate"
            else None
        ),
        "functional_description": (
            execution_freeze["interpretation_contract"]["positive_functional_description"]
            if terminal == "supported_bounded_candidate"
            else None
        ),
        "plurality_resolution": plurality,
        "blocked_claims": list(execution_freeze["interpretation_contract"]["blocked_claims"]),
        "n29_metric_equivalence_claimed": False,
        "load_bearing_external_producer": False,
    }
    result["analysis_digest"] = digest_value(result)
    return result
