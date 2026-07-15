#!/usr/bin/env python3
"""One-shot, fresh-process runtime campaign for P2-I2 Appendix B."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
import tempfile
from typing import Any, Mapping

from p2_i2_app_b_analysis import (
    analyze_receipts,
    build_arm_registry,
    canonical_bytes,
    digest_value,
)


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
REGISTRATION_REL = f"{EXPERIMENT_REL}/contracts/p2-i2/i06-three-mode-registration.json"
MACHINE_POLICY_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json"
PARENT_POLICY_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json"
RUNNER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_run.py"
ANALYSIS_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_analysis.py"
ADAPTER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_history_adapter.py"
REGISTRATION_SCRIPT_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_i06_registration.py"
ARRIVAL_SOURCE_SHA256 = "14d99292e18e2fe34e0fd5c6a1f69051e82115a051d142f10792775e2321e58f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(directory: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(directory), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def _total_coherence(model: Any) -> float:
    return sum(float(node.coherence) for node in model.get_state().base_state.nodes.values())


def _drain(model: Any, count: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _ in range(count):
        require(bool(model.get_state().packet_ledger.event_queue_records), "queue drained early")
        result = model.step()
        records.append(
            {
                "events": [event.kind for event in result.events],
                "bookkeeping": dict(result.bookkeeping),
            }
        )
    require(not model.get_state().packet_ledger.event_queue_records, "queue not empty after drain")
    return records


def _schedule_packet(
    model: Any,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    *,
    source_role: str,
    target_role: str,
    edge_role: str,
    amount: float,
    departure: float,
    arrival: float,
    scheduler_index: int,
    packet_index: int,
    lineage: str,
) -> dict[str, Any]:
    before_total = _total_coherence(model)
    model.schedule_packet_departure(
        source_node_id=role_ids[source_role],
        target_node_id=role_ids[target_role],
        edge_id=edge_ids[edge_role],
        amount=float(amount),
        departure_event_time_key=float(departure),
        arrival_event_time_key=float(arrival),
        scheduler_event_index=int(scheduler_index),
        packet_index=int(packet_index),
        source_lineage_id=f"{lineage}:source",
        target_lineage_id=f"{lineage}:target",
    )
    steps = _drain(model, 2)
    after_total = _total_coherence(model)
    packet = model.get_state().packet_ledger.packet_records[-1].to_record()
    return {
        "processed_event_kinds": [event for step in steps for event in step["events"]],
        "steps": steps,
        "packet_record": packet,
        "max_abs_budget_error": abs(after_total - before_total),
    }


def _appendix_adapter(
    registration: Mapping[str, Any],
    mode: str,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
) -> Any:
    from p2_i2_app_b_history_adapter import RCAEAppendixBHistoryAdapter

    profile = registration["history_adapter_profiles"][
        "history_common" if mode == "history_carried" else "hybrid_common"
    ]
    contribution = registration["contribution_and_schedule"]
    q1, q2 = contribution["contributions"]
    debit = contribution["state_debit"]
    operations = [
        {
            "operation": "G",
            "source_node_id": role_ids[q1["source_role"]],
            "target_node_id": role_ids[q1["common_target_role"]],
            "edge_id": edge_ids[q1["common_edge_role"]],
            "amount": q1["amount"],
        },
        {
            "operation": "E",
            "source_node_id": role_ids[debit["source_role"]],
            "target_node_id": role_ids[debit["target_role"]],
            "edge_id": edge_ids[debit["edge_role"]],
            "amount": debit["amount"],
        },
        {
            "operation": "P",
            "source_node_id": role_ids[q2["source_role"]],
            "target_node_id": role_ids[q2["common_target_role"]],
            "edge_id": edge_ids[q2["common_edge_role"]],
            "amount": q2["amount"],
        },
    ]
    return RCAEAppendixBHistoryAdapter(
        carrier_id=f"p2-i2-app-b-{mode}-H_C",
        pool_target_node_id=role_ids["P"],
        registered_source_node_ids=[role_ids["S1"], role_ids["P"], role_ids["S2"]],
        readout_node_id=role_ids[profile["readout_role"]],
        positive_reservoir_node_id=role_ids[profile["positive_reservoir_role"]],
        negative_sink_node_id=role_ids[profile["negative_sink_role"]],
        positive_edge_id=edge_ids[profile["positive_edge_role"]],
        negative_edge_id=edge_ids[profile["negative_edge_role"]],
        recency_coefficient=float(profile["recency_coefficient"]),
        materialization_tolerance=float(profile["materialization_tolerance"]),
        operation_registry=operations,
    )


def _operation_route(operation: str, selected: bool, private: bool) -> tuple[str, str, str, float]:
    if operation == "G":
        if selected:
            return "S1", "P", "S1_TO_P", 0.625
        if private:
            return "S1", "P1_PRIVATE", "S1_TO_P1_PRIVATE", 0.625
        return "S1", "K_DIV_Q1", "S1_TO_K_DIV_Q1", 0.625
    if operation == "E":
        if selected:
            return "P", "K_P", "P_TO_K_P", 0.4375
        return "E_SOURCE", "E_TARGET", "E_SOURCE_TO_E_TARGET", 0.4375
    if operation == "P":
        if selected:
            return "S2", "P", "S2_TO_P", 0.875
        if private:
            return "S2", "P2_PRIVATE", "S2_TO_P2_PRIVATE", 0.875
        return "S2", "K_DIV_Q2", "S2_TO_K_DIV_Q2", 0.875
    raise AssertionError("unknown operation")


def _participant_lineage(assignment: str, operation: str) -> str:
    mappings = {
        "cyclic_A": {"G": "actor-1", "E": "actor-2", "P": "actor-3"},
        "one_source": {"G": "actor-1", "E": "actor-1", "P": "actor-1"},
        "rotation_B": {"G": "actor-2", "E": "actor-3", "P": "actor-1"},
        "rotation_C": {"G": "actor-3", "E": "actor-1", "P": "actor-2"},
        "label_permutation": {"G": "label-z", "E": "label-x", "P": "label-y"},
    }
    selected = mappings.get(assignment, mappings["cyclic_A"])
    require(operation in selected, "participant operation mapping drifted")
    return f"app-b:participant:{selected[operation]}"


def _pair_identity(registration: Mapping[str, Any], mode: str, model: Any, adapter: Any, roles: Mapping[str, int], edges: Mapping[str, int]) -> dict[str, Any]:
    from p2_i2_i06_registration import _composite_identity

    return _composite_identity(registration, mode, model, adapter, roles, edges)


def _history_receipt(adapter: Any, appended: list[dict[str, Any]]) -> dict[str, Any]:
    tokens = [] if adapter is None else list(adapter.tokens)
    return {
        "tokens": tokens,
        "token_digest": digest_value(tokens),
        "physical_admission_receipts": appended,
        "source_label_free": True,
        "active_history_owner": None if adapter is None else type(adapter).__name__,
    }


def _build_envelope(
    *,
    row: Mapping[str, Any],
    B_before: float,
    B_after: float,
    scheduled: bool,
    response_packet: Mapping[str, Any] | None,
    producer_receipt: Mapping[str, Any],
    carrier_digest: str,
    pre_queue_digest: str,
    post_queue_digest: str,
    tolerance: float,
) -> dict[str, Any]:
    gain = B_after - B_before
    record_id = f"app-b:{row['arm_id']}"
    packet_id = None if response_packet is None else str(response_packet["packet_id"])
    departure_id = None if response_packet is None else str(response_packet["departure_event_id"])
    arrival_id = None if response_packet is None else str(response_packet["arrival_event_id"])
    producer_digest = digest_value(producer_receipt)
    status = "observed_response" if scheduled else "scientific_no_response"
    event_kinds = ["packet_departure", "packet_arrival"] if scheduled else ["event_queue_empty", "event_queue_empty"]
    return {
        "i04r1_response_record": {
            "record_id": record_id,
            "mode": row["mode"],
            "seed": row["seed"],
            "physical_order_id": "q1_then_q2",
            "cell_id": "app-b-eight-arm-subset-matrix",
            "branch_id": row["subset"],
            "pairing_identity": f"app-b:{row['mode']}:seed-{row['seed']}:GEP-order",
            "opportunity_id": "app-b-fixed-GEP-response-opportunity",
            "response_id": "fixed_window_native_B_target_coherence_gain",
            "unit": "native_coherence_amount",
            "status": status,
            "B_before": B_before,
            "B_after": B_after,
            "raw_response": gain,
            "oriented_response": gain,
            "carrier_state_digest": carrier_digest,
            "window_protocol_id": "p2-i2-native-response-window-v2",
            "pre_packet_queue_length": 0,
            "pre_birth_queue_length": 0,
            "post_packet_queue_length": 0,
            "post_birth_queue_length": 0,
            "feedback_surface_call_count": 1,
            "producer_call_count": 1,
            "step_call_count": 2,
            "step_processed_event_kinds": event_kinds,
            "producer_reason": str(producer_receipt["reason_code"]),
            "response_packet_id": packet_id,
            "departure_event_id": departure_id,
            "arrival_event_id": arrival_id,
            "response_packet_amount": 0.125 if scheduled else None,
            "runtime_tolerance": tolerance,
            "B_targeting_event_ids": [] if arrival_id is None else [arrival_id],
            "native_chain_evidence_refs": [] if not scheduled else [producer_digest, departure_id, arrival_id],
            "operational_failure_id": None,
        },
        "window_validity_receipt": {
            "feedback_evaluation_id": f"{record_id}:feedback",
            "feedback_policy_id": "p2-i2-app-b-mode-threshold-v1",
            "producer_invocation_id": f"{record_id}:producer",
            "producer_invocation_receipt_sha256": producer_digest,
            "pre_queue_identity_sha256": pre_queue_digest,
            "post_queue_identity_sha256": post_queue_digest,
            "step_processed_event_ids": [departure_id, arrival_id],
            "window_contamination_event_ids": [],
        },
        "arrival_gain_receipt": {
            "native_coherence_domain_id": "p2-i2-i06-native-closed-coherence-interval",
            "native_coherence_domain_lower": 0.0,
            "native_coherence_domain_upper": 9.25,
            "expected_native_arrival_gain": 0.125 if scheduled else 0.0,
            "arrival_transform_id": "identity_packet_amount_addition" if scheduled else "no_arrival",
            "arrival_semantics_source_sha256": ARRIVAL_SOURCE_SHA256,
            "arrival_semantics_receipt_sha256": digest_value(response_packet or {"no_arrival": True, "arm_id": row["arm_id"]}),
            "arrival_adjustment_event_ids": [],
        },
    }


def execute_arm(root: Path, graph_root: Path, freeze: Mapping[str, Any], row: Mapping[str, Any]) -> dict[str, Any]:
    scripts = root / EXPERIMENT_REL / "scripts"
    graph_source = graph_root / "src"
    sys.path.insert(0, str(scripts)) if str(scripts) not in sys.path else None
    sys.path.insert(0, str(graph_source)) if str(graph_source) not in sys.path else None
    import pygrc
    from pygrc.models import (
        LGRC9V3,
        LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY,
        LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED,
    )
    from p2_i2_app_b_history_adapter import RCAEAppendixBHistoryAdapter
    from p2_i2_i06_registration import _build_model

    require(Path(pygrc.__file__).resolve().is_relative_to(graph_source.resolve()), "PyGRC import is not checkout-bound")
    registration = load_json(root / REGISTRATION_REL)
    mode = str(row["mode"])
    model, role_ids, edge_ids, _ = _build_model(registration, mode)
    adapter = None if mode == "state_carried" else _appendix_adapter(registration, mode, role_ids, edge_ids)
    threshold = float(freeze["mode_realizations"][mode]["feedback_threshold"])
    producer = registration["response_registration"]["producer_primary"]
    model.set_feedback_coupled_pulse_producer(
        source_node_id=role_ids[producer["source_role"]],
        target_node_id=role_ids[producer["target_role"]],
        edge_id=edge_ids[producer["edge_role"]],
        threshold=threshold,
        packet_amount=float(producer["packet_amount"]),
        expected_polarity="positive",
        expected_source_surface_digest=None,
        arrival_event_time_key=16.875,
        enabled=True,
    )
    model.rebase_reset_baseline()
    baseline_identity = _pair_identity(registration, mode, model, adapter, role_ids, edge_ids)
    appended: list[dict[str, Any]] = []
    operation_receipts: list[dict[str, Any]] = []
    private = row["arm_id"].endswith(":private_partition")
    for slot, operation in enumerate(row["operation_order"]):
        selected = operation in set(row["common_operations"])
        source, target, edge, amount = _operation_route(operation, selected, private)
        participant = str(row["participant_assignment"])
        lineage = _participant_lineage(participant, operation)
        scheduled = _schedule_packet(
            model,
            role_ids,
            edge_ids,
            source_role=source,
            target_role=target,
            edge_role=edge,
            amount=amount,
            departure=10.25 + 1.25 * slot,
            arrival=10.875 + 1.25 * slot,
            scheduler_index=20 + slot,
            packet_index=20 + slot,
            lineage=lineage,
        )
        operation_receipts.append(
            {
                "operation": operation,
                "selected_common": selected,
                "source_role": source,
                "target_role": target,
                "edge_role": edge,
                "amount": amount,
                "participant_assignment": participant,
                "participant_lineage": lineage,
                **scheduled,
            }
        )
        if adapter is not None:
            appended.extend(adapter.ingest_new_rows(model))

    intervention = str(row["intervention"])
    history_intervention = None
    if adapter is not None and intervention in {"carrier_clamp", "history_to_reference", "state_and_history_to_reference"}:
        history_intervention = adapter.replace_history(
            (),
            intervention_id=f"{row['arm_id']}:history-reference",
            reason="frozen Appendix B history-component intervention",
        )
    materialization = None
    if adapter is not None:
        materialization = adapter.materialize_readout(
            model,
            departure_event_time_key=14.0,
            arrival_event_time_key=14.625,
            scheduler_event_index=23,
            packet_index=23,
        )

    P_before_intervention = float(model.get_state().base_state.nodes[role_ids["P"]].coherence)
    state_intervention = None
    if intervention in {"carrier_clamp", "state_to_reference_after_history", "state_and_history_to_reference"} and not math.isclose(P_before_intervention, 0.75, rel_tol=0.0, abs_tol=0.0):
        require(P_before_intervention > 0.75, "frozen state intervention requires only native debit")
        state_intervention = _schedule_packet(
            model,
            role_ids,
            edge_ids,
            source_role="P",
            target_role="K_P",
            edge_role="P_TO_K_P",
            amount=P_before_intervention - 0.75,
            departure=14.75,
            arrival=15.0,
            scheduler_index=24,
            packet_index=24,
            lineage=f"app-b:{row['arm_id']}:state-intervention",
        )

    neutral = registration["contribution_and_schedule"]["neutral_contact"]
    neutral_receipt = _schedule_packet(
        model,
        role_ids,
        edge_ids,
        source_role=neutral["source_role"],
        target_role=neutral["target_role"],
        edge_role=neutral["edge_role"],
        amount=float(neutral["amount"]),
        departure=15.25,
        arrival=15.875,
        scheduler_index=25,
        packet_index=25,
        lineage="app-b:neutral",
    )
    state_before = model.get_state()
    require(not state_before.packet_ledger.event_queue_records and not state_before.boundary_birth_trial_queue, "pre-window queue not empty")
    B_before = float(state_before.base_state.nodes[role_ids["B"]].coherence)
    pre_queue_digest = digest_value({"packet": [], "birth": []})
    carrier_identity = _pair_identity(registration, mode, model, adapter, role_ids, edge_ids)
    front_roles = freeze["mode_realizations"][mode]["response_front"]
    feedback = model.emit_feedback_eligibility_surface_row(
        front_node_ids=tuple(role_ids[role] for role in front_roles),
        rear_node_ids=(role_ids["B_REF"],),
        reference_delta=float(registration["response_registration"]["reference_delta"]),
        feedback_threshold=threshold,
        expected_next_route_id=None,
        expected_next_channel_id=None,
    )
    controller = row["arm_id"].endswith(":controller_substitution")
    if controller:
        response_direct = _schedule_packet(
            model,
            role_ids,
            edge_ids,
            source_role="A_PRIMARY",
            target_role="B",
            edge_role="A_PRIMARY_TO_B",
            amount=0.125,
            departure=16.25,
            arrival=16.875,
            scheduler_index=26,
            packet_index=26,
            lineage="app-b:controller-substitution",
        )
        response_steps = response_direct["steps"]
        scheduled = True
        producer_receipt = {
            "reason_code": "controller_authored_direct_native_schedule",
            "scheduled": True,
            "controller_authored": True,
            "common_carrier_reads": [],
        }
    else:
        produced = model.produce_events(
            policy=LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY
        )
        require(len(produced.production_records) == 1, "expected one native producer record")
        production = produced.production_records[0]
        scheduled = production.reason_code == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED
        response_steps = []
        for _ in range(2):
            step = model.step()
            response_steps.append(
                {"events": [event.kind for event in step.events], "bookkeeping": dict(step.bookkeeping)}
            )
        require(not model.get_state().packet_ledger.event_queue_records, "response queue not empty")
        producer_receipt = {
            "reason_code": str(production.reason_code),
            "scheduled": scheduled,
            "controller_authored": False,
            "observed_evidence": dict(production.observed_evidence),
        }

    state_after = model.get_state()
    require(not state_after.packet_ledger.event_queue_records and not state_after.boundary_birth_trial_queue, "post-window queue not empty")
    B_after = float(state_after.base_state.nodes[role_ids["B"]].coherence)
    tolerance = float(registration["response_registration"]["response_gain_tolerance"])
    expected_gain = 0.125 if scheduled else 0.0
    gain = B_after - B_before
    gain_matches = math.isclose(gain, expected_gain, rel_tol=0.0, abs_tol=tolerance)
    require(gain_matches, "B response gain drifted")
    B_packets = [
        packet.to_record()
        for packet in state_after.packet_ledger.packet_records
        if int(packet.target_node_id) == role_ids["B"]
    ]
    require(len(B_packets) == int(scheduled), "B-targeting packet count drifted")
    response_packet = B_packets[0] if B_packets else None
    post_queue_digest = digest_value({"packet": [], "birth": []})
    envelope = _build_envelope(
        row=row,
        B_before=B_before,
        B_after=B_after,
        scheduled=scheduled,
        response_packet=response_packet,
        producer_receipt=producer_receipt,
        carrier_digest=carrier_identity["digest"],
        pre_queue_digest=pre_queue_digest,
        post_queue_digest=post_queue_digest,
        tolerance=tolerance,
    )

    identity_before_save = _pair_identity(registration, mode, model, adapter, role_ids, edge_ids)["digest"]
    with tempfile.TemporaryDirectory(prefix="p2-i2-app-b-") as directory:
        native_path = Path(directory) / "native.json"
        adapter_path = Path(directory) / "adapter.json"
        model.save(str(native_path))
        if adapter is not None:
            adapter.save(adapter_path)
        loaded_model = LGRC9V3.load(str(native_path))
        loaded_adapter = None if adapter is None else RCAEAppendixBHistoryAdapter.load(adapter_path)
        identity_after_load = _pair_identity(registration, mode, loaded_model, loaded_adapter, role_ids, edge_ids)["digest"]
        loaded_model.reset()
        if loaded_adapter is not None:
            loaded_adapter.reset()
        identity_after_reset = _pair_identity(registration, mode, loaded_model, loaded_adapter, role_ids, edge_ids)["digest"]

    history = _history_receipt(adapter, appended)
    return {
        "arm_id": row["arm_id"],
        "arm_row_digest": digest_value(row),
        "process_receipt": {
            "fresh_process": True,
            "pid": os.getpid(),
            "logical_executable": ".venv/bin/python",
            "pygrc_source": "external-repository:graph-reflexive-coherence/src",
            "dont_write_bytecode": sys.dont_write_bytecode,
        },
        "baseline": {
            "fresh_model": True,
            "node_count": len(role_ids),
            "edge_count": len(edge_ids),
            "identity": baseline_identity["digest"],
        },
        "operation_receipts": operation_receipts,
        "history_receipt": history,
        "history_materialization": materialization,
        "history_intervention": history_intervention,
        "state_intervention": state_intervention,
        "carrier_receipt": {
            "P_before_intervention": P_before_intervention,
            "P_after": float(state_before.base_state.nodes[role_ids["P"]].coherence),
            "M_H_after": float(state_before.base_state.nodes[role_ids["M_H"]].coherence),
            "front_roles": list(front_roles),
        },
        "neutral_receipt": neutral_receipt,
        "response_receipt": {
            "boundary_score": float(feedback.surface_values_after["boundary_polarity_score"]),
            "threshold": threshold,
            "scheduled": scheduled,
            "controller_authored": controller,
            "B_before": B_before,
            "B_after": B_after,
            "gain": gain,
            "expected_gain": expected_gain,
            "gain_matches": gain_matches,
            "window_valid": True,
            "queue_empty_after": True,
            "response_steps": response_steps,
            "producer_receipt": producer_receipt,
        },
        "response_envelope": envelope,
        "restoration_receipt": {
            "identity_before_save": identity_before_save,
            "identity_after_load": identity_after_load,
            "identity_after_reset": identity_after_reset,
        },
        "resource_receipt": {
            "node_count": len(role_ids),
            "edge_count": len(edge_ids),
            "maximum_queue_length": 1,
            "packet_count": len(state_after.packet_ledger.packet_records),
        },
        "scientific_interpretation": None,
    }


def _preflight(args: argparse.Namespace, freeze: Mapping[str, Any], graph_root: Path) -> dict[str, Any]:
    require(all(portable_relative(value) for value in (args.freeze, args.claim, args.output, args.graph_root)), "absolute path refused")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "-B is required")
    head = git(ROOT, "rev-parse", "HEAD")
    require(head == args.expected_head, "authority HEAD drifted")
    require(git(graph_root, "rev-parse", "HEAD") == freeze["environment"]["graph_commit"], "graph HEAD drifted")
    require(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph worktree dirty")
    claim_rel = args.claim
    output_rel = args.output
    status = git(ROOT, "status", "--porcelain=v1", "--untracked-files=all")
    require(status == "", "authority worktree must be clean before claim")
    require(not (ROOT / claim_rel).exists(), "campaign claim already exists")
    require(not (ROOT / output_rel).exists(), "governed output already exists")
    for item in freeze["authority_inputs"]:
        require(sha256(ROOT / item["path"]) == item["sha256"], f"authority drift: {item['path']}")
    for relative, expected in freeze["implementation_sha256"].items():
        require(sha256(ROOT / relative) == expected, f"implementation drift: {relative}")
    executable = Path(sys.executable).resolve()
    require(sha256(executable) == freeze["environment"]["interpreter_sha256"], "interpreter drift")
    normalized = [
        ".venv/bin/python", "-B", RUNNER_REL,
        "--freeze", args.freeze,
        "--claim", args.claim,
        "--output", args.output,
        "--expected-head", args.expected_head,
        "--graph-root", args.graph_root,
    ]
    expected_command = [
        args.expected_head if item == "{AUTHORITY_HEAD}" else item
        for item in freeze["execution"]["normalized_command_template"]
    ]
    require(normalized == expected_command, "command drifted")
    return {
        "authority_head": head,
        "authority_clean_before_claim": True,
        "graph_commit": freeze["environment"]["graph_commit"],
        "graph_clean": True,
        "interpreter_sha256": freeze["environment"]["interpreter_sha256"],
        "normalized_command": normalized,
    }


def _claim(path: Path, receipt: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(canonical_bytes(receipt))
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        raise


def parent_main(args: argparse.Namespace) -> int:
    freeze = load_json(ROOT / args.freeze)
    graph_root = (ROOT / args.graph_root).resolve()
    preflight = _preflight(args, freeze, graph_root)
    rows = build_arm_registry(freeze["arm_registry_specification"])
    claim = {
        "artifact_id": "P2-I2-APP-B2-CAMPAIGN-CLAIM",
        "authorization_consumed": True,
        "governed_attempt": 1,
        "scientific_retries_allowed": 0,
        "infrastructure_retries_allowed": 0,
        "preflight": preflight,
        "freeze_sha256": sha256(ROOT / args.freeze),
        "arm_registry_digest": digest_value(rows),
        "output_path": args.output,
    }
    _claim(ROOT / args.claim, claim)
    receipts: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        worker = subprocess.run(
            [
                str(Path(sys.executable).resolve()), "-B", str(ROOT / RUNNER_REL),
                "--worker", "--freeze", args.freeze,
                "--graph-root", args.graph_root,
                "--row-json", json.dumps(row, sort_keys=True, separators=(",", ":")),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        receipt = json.loads(worker.stdout)
        require(receipt["arm_id"] == row["arm_id"], "worker returned wrong arm")
        receipts.append(receipt)
        if (index + 1) % 10 == 0:
            print(f"completed {index + 1}/{len(rows)} arms", file=sys.stderr, flush=True)
    machine = load_json(ROOT / MACHINE_POLICY_REL)
    parent = load_json(ROOT / PARENT_POLICY_REL)
    analysis = analyze_receipts(receipts, freeze, machine, parent)
    result = {
        "artifact_id": "P2-I2-APP-B2-RUNTIME-EVIDENCE",
        "artifact_version": "1.0",
        "authority": claim,
        "arm_count": len(receipts),
        "receipts": receipts,
        "analysis": analysis,
        "runtime_invocation_count": 1,
        "scientific_retry_count": 0,
        "candidate_parameter_search_count": 0,
        "graph_repository_mutation_count": 0,
    }
    result["canonical_payload_digest"] = digest_value(result)
    output = ROOT / args.output
    output.write_bytes(canonical_bytes(result))
    require(load_json(output) == result, "governed output readback mismatch")
    print(json.dumps({"status": "complete", "arms": len(receipts), "analysis": analysis["terminal_classification"]}))
    return 0


def worker_main(args: argparse.Namespace) -> int:
    require(args.row_json is not None, "worker row is required")
    freeze = load_json(ROOT / args.freeze)
    row = json.loads(args.row_json)
    receipt = execute_arm(ROOT, (ROOT / args.graph_root).resolve(), freeze, row)
    sys.stdout.buffer.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--claim")
    parser.add_argument("--output")
    parser.add_argument("--expected-head")
    parser.add_argument("--graph-root", required=True)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--row-json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.worker:
        return worker_main(args)
    require(all((args.claim, args.output, args.expected_head)), "parent authority arguments required")
    return parent_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
