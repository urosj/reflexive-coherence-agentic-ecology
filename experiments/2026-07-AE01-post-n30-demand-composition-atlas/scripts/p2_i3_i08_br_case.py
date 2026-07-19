#!/usr/bin/env python3
"""Execute exactly one supervisor-authorized P2-I3 B-R governed entry.

This module is live-operation code and is never imported by the I07 builder or
supervisor.  A fresh ``python -B`` child imports it only after a durable case
claim and a matching supervisor-owned P5 authorization exist.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
from typing import Any, Mapping, Sequence

import pygrc
from pygrc.models import (
    LGRC9V3,
    compute_lgrc9v3_causal_distances,
    compute_lgrc9v3_functional_distances,
    compute_lgrc9v3_geometric_distances,
    digest_lgrc9v3_restoration_identity_v2,
    lgrc9v3_restoration_identity_v2,
)

from p2_i3_br_execution_runtime import (
    POLICY_REL,
    ROOT,
    canonical_bytes,
    ensure_no_symlink_components,
    load_json,
    payload_digest,
    require,
    sha256_file,
    verify_digest,
    with_digest,
    write_exclusive_json,
)
from p2_i3_br_runtime import (
    build_blind_encounter_request,
    evaluate_export_policy,
    initial_policy_state,
    settle_export_policy,
)
from p2_i3_i06_br_registration import build_baseline_model


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
REGISTRATION_REL = EXPERIMENT / "contracts/p2-i3/i06-br-exact-registration.json"
MATRIX_REL = EXPERIMENT / "contracts/p2-i3/i07-br-run-matrix.json"
FREEZE_REL = EXPERIMENT / "contracts/p2-i3/i07-br-inactive-exec-freeze.json"
TOLERANCE = 1e-12


def native_state(model: LGRC9V3) -> Any:
    return model.get_state()


def native_identity_digest(model: LGRC9V3) -> str:
    return digest_lgrc9v3_restoration_identity_v2(model)


def native_identity_record(model: LGRC9V3) -> dict[str, Any]:
    return lgrc9v3_restoration_identity_v2(model)


def node_coherences(model: LGRC9V3) -> dict[int, float]:
    state = native_state(model)
    return {
        int(node_id): float(node.coherence)
        for node_id, node in sorted(state.base_state.nodes.items())
    }


def budget_record(model: LGRC9V3) -> dict[str, float]:
    ledger = native_state(model).packet_ledger
    require(ledger is not None, "native packet ledger missing")
    return {
        "node_coherence_total": float(ledger.node_coherence_total),
        "in_flight_packet_total": float(ledger.in_flight_packet_total),
        "conserved_budget_total": float(ledger.conserved_budget_total),
        "budget_error": float(ledger.budget_error),
    }


def processing_receipt(result: Any) -> dict[str, Any]:
    for event in result.events:
        processed = event.payload.get("processed_event")
        packet = event.payload.get("packet_record")
        if isinstance(processed, dict) and isinstance(packet, dict):
            return {
                "event_kind": processed["event_kind"],
                "event_id": processed["event_id"],
                "event_time_key": float(processed["event_time_key"]),
                "scheduler_event_index": int(processed["scheduler_event_index"]),
                "edge_id": int(processed["edge_id"]),
                "source_node_id": int(processed["source_node_id"]),
                "target_node_id": int(processed["target_node_id"]),
                "amount": float(processed["amount"]),
                "packet_id": processed["packet_id"],
                "source_lineage_id": packet.get("source_lineage_id"),
                "target_lineage_id": packet.get("target_lineage_id"),
                "budget_error": float(event.payload.get("budget_error", 0.0)),
            }
    raise RuntimeError("native result lacks a processed packet event")


def schedule_registered_packet(model: LGRC9V3, request: Mapping[str, Any]) -> None:
    model.schedule_packet_departure(
        source_node_id=int(request["source_node_id"]),
        target_node_id=int(request["target_node_id"]),
        edge_id=int(request["edge_id"]),
        amount=float(request["amount"]),
        departure_event_time_key=float(request["departure_event_time_key"]),
        arrival_event_time_key=float(request["arrival_event_time_key"]),
        scheduler_event_index=int(request["scheduler_event_index"]),
        packet_index=int(request["packet_index"]),
        source_lineage_id=str(request["source_lineage_id"]),
        target_lineage_id=str(request["target_lineage_id"]),
    )


def run_registered_event(model: LGRC9V3) -> Any:
    return model.step()


def drain_registered_queue(model: LGRC9V3, *, max_events: int = 2) -> list[Any]:
    return model.run_event_queue(max_events=max_events)


def native_observation(model: LGRC9V3) -> dict[str, Any]:
    snapshot = model.snapshot()
    return {
        "restoration_v2_digest": native_identity_digest(model),
        "coherences": {str(key): value for key, value in node_coherences(model).items()},
        "budget": budget_record(model),
        "snapshot_digest": hashlib.sha256(canonical_bytes(snapshot)).hexdigest(),
    }


def distance_annotations(model: LGRC9V3, source_node_id: int) -> dict[str, Any]:
    runtime = native_state(model)
    base = runtime.base_state
    causal_delay = {int(edge_id): float(value) for edge_id, value in base.temporal_delay.items()}
    return {
        "geometric": {str(key): value for key, value in compute_lgrc9v3_geometric_distances(base, source_node_id=source_node_id).items()},
        "functional": {str(key): value for key, value in compute_lgrc9v3_functional_distances(base, source_node_id=source_node_id).items()},
        "causal": {str(key): value for key, value in compute_lgrc9v3_causal_distances(base, source_node_id=source_node_id, edge_causal_delay=causal_delay).items()},
        "scientific_substitution_allowed": False,
    }


def topology_for(registration: Mapping[str, Any], realization: int) -> dict[str, Any]:
    matches = [row for row in registration["candidate_design"]["topology_by_realization"] if row["realization_id"] == realization]
    require(len(matches) == 1, "realization topology is not unique")
    return matches[0]


def roles(topology: Mapping[str, Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in topology["node_role_to_raw_id"].items()}


def edges(topology: Mapping[str, Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in topology["edge_role_to_raw_id"].items()}


def request(
    *,
    topology: Mapping[str, Any],
    source_role: str,
    target_role: str,
    edge_role: str,
    amount: float,
    departure: float,
    delay: float,
    scheduler_index: int,
    packet_index: int,
    lineage: str,
) -> dict[str, Any]:
    node_roles = roles(topology)
    edge_roles = edges(topology)
    return {
        "source_node_id": node_roles[source_role],
        "target_node_id": node_roles[target_role],
        "edge_id": edge_roles[edge_role],
        "amount": amount,
        "departure_event_time_key": departure,
        "arrival_event_time_key": departure + delay,
        "scheduler_event_index": scheduler_index,
        "packet_index": packet_index,
        "source_lineage_id": f"{lineage}:source",
        "target_lineage_id": f"{lineage}:target",
    }


def execute_transfer(model: LGRC9V3, packet: Mapping[str, Any]) -> dict[str, Any]:
    before = native_observation(model)
    schedule_registered_packet(model, packet)
    results = drain_registered_queue(model, max_events=2)
    require(len(results) == 2, "registered transfer did not produce departure and arrival")
    receipts = [processing_receipt(row) for row in results]
    after = native_observation(model)
    require(abs(after["budget"]["budget_error"]) <= TOLERANCE, "registered transfer broke global budget")
    return {"request": deepcopy(dict(packet)), "before": before, "events": receipts, "after": after}


def policy_binding(topology: Mapping[str, Any], route: str, delay: float) -> dict[str, Any]:
    node_roles = roles(topology)
    edge_roles = edges(topology)
    schedules = {}
    for sequence, (time_key, scheduler_index) in enumerate(((12, 12), (16, 16), (20, 20), (24, 24))):
        schedules[str(sequence)] = {
            "departure_event_time_key": float(time_key),
            "arrival_event_time_key": float(time_key) + delay,
            "scheduler_event_index": scheduler_index,
            "packet_index": sequence,
            "source_lineage_id": f"p2-i3-br:{route}:export:{sequence}:source",
            "target_lineage_id": f"p2-i3-br:{route}:export:{sequence}:target",
        }
    return {
        "policy_id": f"P2-I3-BR-POLICY-{route}",
        "route_id": route,
        "source_node_id": node_roles[f"{route}_m"],
        "destination_node_id": node_roles[f"{route}_d"],
        "edge_id": edge_roles[f"{route}_export"],
        "export_floor": 3.0 / 16.0,
        "export_cap": 3.0 / 32.0,
        "absolute_tolerance": TOLERANCE,
        "schedule_by_sequence": schedules,
    }


def lifecycle_receipt(
    *, receipt_id: str, sequence: int, predecessor: str, policy_state: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "schema": "p2_i3_br_lifecycle_receipt_v1",
        "receipt_id": receipt_id,
        "route_id": policy_state["route_id"],
        "sequence_index": sequence,
        "qualifying_native_event_identity": f"P2-I3-BR-LIFECYCLE-{sequence}",
        "predecessor_composite_identity": predecessor,
        "policy_id": policy_state["policy_id"],
        "source_node_id": policy_state["source_node_id"],
        "destination_node_id": policy_state["destination_node_id"],
        "edge_id": policy_state["edge_id"],
        "prior_settlement_status": "settled",
        "eligible": True,
    }


def construct_registered_control_state(
    model: LGRC9V3,
    *,
    topology: Mapping[str, Any],
    family: str,
    focal_route: str,
    reference_route: str,
) -> LGRC9V3:
    """Construct only the exact evidence-only state interventions in DEC-044."""

    if family not in {
        "current_state_relocation",
        "carrier_matched_false_trace",
        "causal_projection_matched_false_trace",
    }:
        return model
    state = deepcopy(native_state(model))
    node_roles = roles(topology)
    if family == "current_state_relocation":
        for suffix in ("s", "m", "x", "d", "z_s", "z_m"):
            left = node_roles[f"{focal_route}_{suffix}"]
            right = node_roles[f"{reference_route}_{suffix}"]
            state.base_state.nodes[left], state.base_state.nodes[right] = (
                state.base_state.nodes[right],
                state.base_state.nodes[left],
            )
    elif family == "carrier_matched_false_trace":
        source = node_roles[f"{focal_route}_s"]
        carrier = node_roles[f"{focal_route}_m"]
        state.base_state.nodes[source].coherence = 19.0 / 32.0
        state.base_state.nodes[carrier].coherence = 9.0 / 32.0
    # causal_projection_matched_false_trace deliberately leaves the complete
    # causal native state unchanged; only the separately retained audit
    # provenance changes from attributable formation to false installation.
    return LGRC9V3.from_state(
        state,
        {
            "dt": 1.0,
            "causal_modes": {
                "causal_layer_mode": "packetized_fixed_topology",
                "lgrc_runtime_level": "lgrc2",
                "lapse_policy": "unit",
                "edge_delay_policy": "constant_delay",
                "event_time_policy": "explicit_event_time_key",
                "proper_time_accumulation_policy": "local_event_frontier",
            },
        },
    )


def blob_path(content_store: Path, digest: str) -> Path:
    return content_store / digest[:2] / digest


def retain_blob(content_store: Path, data: bytes) -> dict[str, Any]:
    digest = hashlib.sha256(data).hexdigest()
    path = blob_path(content_store, digest)
    ensure_no_symlink_components(content_store.parent.parent, path.relative_to(content_store.parent.parent))
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(not path.is_symlink() and path.read_bytes() == data, "content-addressed blob collision")
    else:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(descriptor, data)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    return {"sha256": digest, "byte_length": len(data), "content_store_key": f"sha256/{digest[:2]}/{digest}"}


def write_checkpoint_bundle(
    *,
    model: LGRC9V3,
    content_store: Path,
    checkpoint_id: str,
    policy_state: Mapping[str, Any],
    execution_state: Mapping[str, Any],
    measurement_state: Mapping[str, Any],
    reset_state: Mapping[str, Any],
    audit_state: Mapping[str, Any],
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p2-i3-br-native-") as raw:
        native_path = Path(raw) / "native.json"
        model.save(str(native_path))
        native_bytes = native_path.read_bytes()
    native_identity = native_identity_record(model)
    components: dict[str, bytes] = {
        "native.json": native_bytes,
        "native-identity-v2.json": canonical_bytes(native_identity),
        "policy.json": canonical_bytes(policy_state),
        "execution.json": canonical_bytes(execution_state),
        "measurement.json": canonical_bytes(measurement_state),
        "reset.json": canonical_bytes(reset_state),
        "audit.json": canonical_bytes(audit_state),
    }
    retained = {name: retain_blob(content_store, data) for name, data in components.items()}
    payload = {
        "bundle_schema_id": "P2-I3-BR-I06-EIGHT-COMPONENT-BUNDLE-V1",
        "checkpoint_id": checkpoint_id,
        "native_restoration_v2_digest": native_identity_digest(model),
        "components": retained,
    }
    exact_identity = payload_digest(payload)
    manifest = with_digest({**payload, "exact_composite_identity": exact_identity})
    manifest_bytes = canonical_bytes(manifest)
    manifest_blob = retain_blob(content_store, manifest_bytes)
    return {"exact_composite_identity": exact_identity, "manifest": manifest, "manifest_blob": manifest_blob}


def load_checkpoint_bundle(
    *, content_store: Path, manifest: Mapping[str, Any]
) -> tuple[LGRC9V3, dict[str, Any]]:
    verify = deepcopy(dict(manifest))
    require(verify.pop("canonical_payload_digest") == payload_digest(verify), "checkpoint manifest digest mismatch")
    components: dict[str, bytes] = {}
    for name, binding in manifest["components"].items():
        path = blob_path(content_store, binding["sha256"])
        require(path.is_file() and not path.is_symlink(), f"checkpoint blob unavailable: {name}")
        data = path.read_bytes()
        require(len(data) == binding["byte_length"] and hashlib.sha256(data).hexdigest() == binding["sha256"], f"checkpoint blob identity mismatch: {name}")
        components[name] = data
    with tempfile.TemporaryDirectory(prefix="p2-i3-br-load-") as raw:
        path = Path(raw) / "native.json"
        path.write_bytes(components["native.json"])
        model = LGRC9V3.load(str(path))
    require(native_identity_digest(model) == manifest["native_restoration_v2_digest"], "loaded native identity drifted")
    decoded = {
        name: json.loads(data.decode("utf-8"))
        for name, data in components.items()
        if name != "native.json"
    }
    return model, decoded


def verify_registered_reset(model: LGRC9V3, expected_digest: str) -> None:
    model.reset()
    require(native_identity_digest(model) == expected_digest, "native reset identity drifted")


def trajectory_operations(
    *,
    registration: Mapping[str, Any],
    configuration: Mapping[str, Any],
    topology: Mapping[str, Any],
    model: LGRC9V3,
    baseline_identity: str,
    content_store: Path,
) -> dict[str, Any]:
    delay = 1.0 if configuration["delay_profile_id"] == "tau-1" else 2.0
    require(native_identity_digest(model) == baseline_identity, "loaded operational baseline identity drifted")
    family = configuration["family_id"]
    focal_route, reference_route = ("B", "A") if family == "focal_reference_role_exchange" else ("A", "B")
    arm = configuration["arm"]
    ledger: list[dict[str, Any]] = []
    formation_times = [8] if family == "formation_quantity_history" else [0, 4, 8]
    formation_amounts = [9.0 / 32.0] if family == "formation_quantity_history" else [3.0 / 32.0] * 3
    formation_indices = [8] if family == "formation_quantity_history" else [0, 4, 8]
    for index, (time_key, amount, scheduler) in enumerate(zip(formation_times, formation_amounts, formation_indices, strict=True)):
        target_suffix = "z_s" if arm == "W" else "m"
        ledger.append(
            execute_transfer(
                model,
                request(
                    topology=topology,
                    source_role=f"{focal_route}_s",
                    target_role=f"{focal_route}_{target_suffix}",
                    edge_role=f"{focal_route}_{'source_control' if arm == 'W' else 'formation'}",
                    amount=amount,
                    departure=float(time_key),
                    delay=delay,
                    scheduler_index=scheduler,
                    packet_index=index,
                    lineage=f"{configuration['configuration_id']}:focal-formation:{index}",
                ),
            )
        )
    for index, (time_key, scheduler) in enumerate(zip((0, 4, 8), (2, 6, 10), strict=True)):
        ledger.append(
            execute_transfer(
                model,
                request(
                    topology=topology,
                    source_role=f"{reference_route}_s",
                    target_role=f"{reference_route}_z_s",
                    edge_role=f"{reference_route}_source_control",
                    amount=3.0 / 32.0,
                    departure=float(time_key),
                    delay=delay,
                    scheduler_index=scheduler,
                    packet_index=index,
                    lineage=f"{configuration['configuration_id']}:reference-activity:{index}",
                ),
            )
        )

    policy = initial_policy_state(policy_binding(topology, focal_route, delay))
    checkpoints: dict[str, Any] = {}
    audit_lineage = {
        "configuration_id": configuration["configuration_id"],
        "formation_classification": (
            "false_installation"
            if family in {"carrier_matched_false_trace", "causal_projection_matched_false_trace"}
            else ("withdrawn" if arm == "W" else "attributable_formation")
        ),
        "forbidden_reads": [],
        "raw_ids_used_for_scientific_selection": False,
    }
    reset_state = {"baseline_native_restoration_v2_digest": baseline_identity, "fresh_branch_lineage_required": True}

    for sequence in range(4):
        predecessor = native_identity_digest(model)
        disposition: dict[str, Any]
        if arm == "W":
            disposition = {"disposition": "eligible_zero", "sequence": sequence, "native_request": None, "policy_invoked": True}
        elif arm == "O":
            disposition = {"disposition": "explicit_neutralization", "sequence": sequence, "native_request": None, "policy_invoked": True}
        elif family == "export_policy_omission":
            disposition = {"disposition": "policy_omitted", "sequence": sequence, "native_request": None, "policy_invoked": False}
        elif family == "lifecycle_schedule_omission":
            disposition = {"disposition": "lifecycle_invocation_omitted", "sequence": sequence, "native_request": None, "policy_invoked": False}
        else:
            receipt_id = f"{configuration['configuration_id']}:lifecycle:{sequence}"
            receipt = lifecycle_receipt(receipt_id=receipt_id, sequence=sequence, predecessor=predecessor, policy_state=policy)
            carrier = node_coherences(model)[roles(topology)[f"{focal_route}_m"]]
            evaluated = evaluate_export_policy(carrier_coherence=carrier, receipt=receipt, predecessor_composite_identity=predecessor, policy_state=policy)
            policy = evaluated["policy_state"]
            disposition = {"disposition": evaluated["disposition"], "sequence": sequence, "policy_invoked": True, "reserved_amount": evaluated.get("reserved_amount", 0.0)}
            if evaluated["native_request"] is not None:
                native_request = deepcopy(evaluated["native_request"])
                if family == "reservoir_clamp":
                    native_request.update(
                        {
                            "target_node_id": roles(topology)[f"{focal_route}_z_m"],
                            "edge_id": edges(topology)[f"{focal_route}_carrier_control"],
                        }
                    )
                    disposition["control_replacement"] = "carrier_sink"
                    ledger.append(execute_transfer(model, native_request))
                elif family == "export_mass_organization":
                    half = float(native_request["amount"]) / 2.0
                    source_control = request(
                        topology=topology,
                        source_role=f"{focal_route}_s",
                        target_role=f"{focal_route}_z_s",
                        edge_role=f"{focal_route}_source_control",
                        amount=half,
                        departure=float(native_request["departure_event_time_key"]),
                        delay=delay,
                        scheduler_index=int(native_request["scheduler_event_index"]),
                        packet_index=int(native_request["packet_index"]),
                        lineage=f"{configuration['configuration_id']}:mass-control:{sequence}:source",
                    )
                    carrier_control = request(
                        topology=topology,
                        source_role=f"{focal_route}_m",
                        target_role=f"{focal_route}_z_m",
                        edge_role=f"{focal_route}_carrier_control",
                        amount=half,
                        departure=float(native_request["departure_event_time_key"]),
                        delay=delay,
                        scheduler_index=int(native_request["scheduler_event_index"]) + 1,
                        packet_index=int(native_request["packet_index"]),
                        lineage=f"{configuration['configuration_id']}:mass-control:{sequence}:carrier",
                    )
                    ledger.extend((execute_transfer(model, source_control), execute_transfer(model, carrier_control)))
                    disposition["control_replacement"] = "equal_mass_zero_organization_contrast"
                else:
                    ledger.append(execute_transfer(model, native_request))
                policy = settle_export_policy(policy, receipt_id=receipt_id, native_settlement_identity=native_identity_digest(model))
                disposition["native_request"] = native_request
            else:
                disposition["native_request"] = None
        ledger.append({"lifecycle": disposition})

        if sequence == 1:
            model = construct_registered_control_state(
                model,
                topology=topology,
                family=family,
                focal_route=focal_route,
                reference_route=reference_route,
            )
        checkpoint = {0: "j1", 1: "j2", 3: "j3"}.get(sequence)
        if checkpoint:
            execution_state = {
                "configuration_id": configuration["configuration_id"],
                "checkpoint": checkpoint,
                "sequence": sequence,
                "future_schedule_id": f"P2-I3-BR-FUTURE-{checkpoint}",
                "operation_ledger_digest": payload_digest({"ledger": ledger}),
            }
            measurement_state = {
                "checkpoint": checkpoint,
                "probe_executed": False,
                "carrier_by_route": {
                    "focal": node_coherences(model)[roles(topology)[f"{focal_route}_m"]],
                    "reference": node_coherences(model)[roles(topology)[f"{reference_route}_m"]],
                },
            }
            checkpoints[checkpoint] = write_checkpoint_bundle(
                model=model,
                content_store=content_store,
                checkpoint_id=f"{configuration['configuration_id']}:{checkpoint}",
                policy_state=policy,
                execution_state=execution_state,
                measurement_state=measurement_state,
                reset_state=reset_state,
                audit_state=audit_lineage,
            )
    return {
        "baseline_native_restoration_v2_digest": baseline_identity,
        "focal_route": focal_route,
        "reference_route": reference_route,
        "operation_ledger": ledger,
        "checkpoints": checkpoints,
        "terminal_native_observation": native_observation(model),
    }


def baseline_parent_row(matrix: Mapping[str, Any], entry: Mapping[str, Any]) -> dict[str, Any]:
    matches = [
        row
        for row in matrix["entries"]
        if row["entry_id"] in entry["parent_entry_ids"]
        and row["entry_kind"] == "operational_baseline_construction"
    ]
    require(len(matches) == 1, "operational baseline parent is not unique")
    return matches[0]


def load_operational_baseline(
    *, matrix: Mapping[str, Any], entry: Mapping[str, Any], content_store: Path
) -> tuple[LGRC9V3, str, dict[str, Any]]:
    parent = baseline_parent_row(matrix, entry)
    parent_manifest_path = ROOT / parent["governed_paths"]["logical_manifest"]
    require(parent_manifest_path.is_file(), "operational baseline logical manifest is missing")
    parent_result = load_json(parent_manifest_path)
    require(
        parent_result["entry_id"] == parent["entry_id"]
        and parent_result["case_id"] is None,
        "operational baseline manifest identity drifted",
    )
    bundle = parent_result["result"]["baseline_bundle"]
    model, components = load_checkpoint_bundle(
        content_store=content_store,
        manifest=bundle["manifest"],
    )
    return model, bundle["manifest"]["native_restoration_v2_digest"], components


def execute_operational_baseline(
    *, registration: Mapping[str, Any], matrix: Mapping[str, Any], entry: Mapping[str, Any], content_store: Path
) -> dict[str, Any]:
    require(entry["case_id"] is None, "operational baseline acquired a scientific case identity")
    require(entry["scientific_evidence_effect"] == "none", "operational baseline acquired scientific evidence effect")
    require(
        all(value == 0 for value in entry["scientific_operation_counts"].values()),
        "operational baseline acquired a scientific operation",
    )
    topology = topology_for(registration, int(entry["realization_id"]))
    delay = 1 if entry["delay_profile_id"] == "tau-1" else 2
    model = build_baseline_model(topology, delay)
    baseline_identity = native_identity_digest(model)
    bundle = write_checkpoint_bundle(
        model=model,
        content_store=content_store,
        checkpoint_id=f"{entry['entry_id']}:operational-baseline",
        policy_state={
            "baseline_kind": "native_plus_rcae",
            "route_policy_templates": {
                route: policy_binding(topology, route, float(delay)) for route in ("A", "B")
            },
            "lifecycle_receipts": [],
        },
        execution_state={
            "entry_id": entry["entry_id"],
            "schedule_ordinal": entry["schedule_ordinal"],
            "produced_restoration_refs": entry["produced_restoration_refs"],
            "pending_events": [],
        },
        measurement_state={
            "formation_operations": 0,
            "export_operations": 0,
            "encounter_operations": 0,
            "scientific_control_operations": 0,
            "integrity_fault_operations": 0,
        },
        reset_state={
            "baseline_native_restoration_v2_digest": baseline_identity,
            "fresh_branch_lineage_required": True,
        },
        audit_state={
            "scientific_evidence_effect": "none",
            "source_runtime_save_load_identity_verified": True,
        },
    )
    loaded, components = load_checkpoint_bundle(
        content_store=content_store,
        manifest=bundle["manifest"],
    )
    require(native_identity_digest(loaded) == baseline_identity, "operational baseline save/load identity drifted")
    verify_registered_reset(loaded, baseline_identity)
    require(native_identity_digest(model) == baseline_identity, "operational baseline construction mutated source model")
    return {
        "baseline_bundle": bundle,
        "baseline_native_restoration_v2_digest": baseline_identity,
        "produced_restoration_refs": entry["produced_restoration_refs"],
        "loaded_component_roles": sorted(components),
        "save_load_reset_verified": True,
        "scientific_operation_counts": deepcopy(entry["scientific_operation_counts"]),
        "scientific_evidence_effect": "none",
    }


def execute_trajectory(
    *,
    registration: Mapping[str, Any],
    matrix: Mapping[str, Any],
    entry: Mapping[str, Any],
    configuration: Mapping[str, Any],
    content_store: Path,
    prepared_model: LGRC9V3,
    prepared_baseline_identity: str,
) -> dict[str, Any]:
    topology = topology_for(registration, int(configuration["realization_id"]))
    return trajectory_operations(
        registration=registration,
        configuration=configuration,
        topology=topology,
        model=prepared_model,
        baseline_identity=prepared_baseline_identity,
        content_store=content_store,
    )


def parent_trajectory_row(matrix: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    parent_id = next(item for item in case["parent_entry_ids"] if item.endswith("-TRAJECTORY"))
    matches = [row for row in matrix["entries"] if row["entry_id"] == parent_id]
    require(len(matches) == 1, "terminal probe parent trajectory is not unique")
    return matches[0]


def execute_probe(
    *,
    registration: Mapping[str, Any],
    matrix: Mapping[str, Any],
    case: Mapping[str, Any],
    configuration: Mapping[str, Any],
    governed_root: Path,
    content_store: Path,
    prepared_model: LGRC9V3,
    prepared_components: Mapping[str, Any],
    prepared_checkpoint_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    checkpoint = str(case["checkpoint"])
    checkpoint_bundle = prepared_checkpoint_bundle
    model = prepared_model
    components = prepared_components
    topology = topology_for(registration, int(configuration["realization_id"]))
    family = configuration["family_id"]
    focal_route, reference_route = ("B", "A") if family == "focal_reference_role_exchange" else ("A", "B")
    selected = focal_route if case["route_role"] == "focal" else reference_route
    node_roles = roles(topology)
    edge_roles = edges(topology)
    source = node_roles[f"{selected}_m"]
    target = node_roles[f"{selected}_x"]
    edge = edge_roles[f"{selected}_encounter"]
    carrier_pre = node_coherences(model)[source]
    q_probe = 15.0 / 64.0
    opportunity = {
        "opportunity_id": case["case_id"],
        "parent_composite_identity": checkpoint_bundle["exact_composite_identity"],
        "source_node_id": source,
        "target_node_id": target,
        "edge_id": edge,
        "amount": q_probe,
        "departure_event_time_key": float({"j1": 16, "j2": 20, "j3": 28}[checkpoint]),
        "arrival_event_time_key": float({"j1": 16, "j2": 20, "j3": 28}[checkpoint]) + (1.0 if configuration["delay_profile_id"] == "tau-1" else 2.0),
        "scheduler_event_index": int({"j1": 16, "j2": 20, "j3": 28}[checkpoint]),
        "packet_index": 0,
        "source_lineage_id": f"{case['case_id']}:source",
        "target_lineage_id": f"{case['case_id']}:target",
    }
    packet = build_blind_encounter_request(opportunity=opportunity, parent_composite_identity=checkpoint_bundle["exact_composite_identity"])
    before_identity = native_identity_digest(model)
    schedule_registered_packet(model, packet)
    scheduled_identity = native_identity_digest(model)
    disposition = "invalid_or_infrastructure_failure"
    refusal_reason = None
    receipts: list[dict[str, Any]] = []
    try:
        departure = run_registered_event(model)
        receipts.append(processing_receipt(departure))
        arrival = run_registered_event(model)
        receipts.append(processing_receipt(arrival))
        disposition = "admitted"
    except Exception as exc:
        require(type(exc).__module__ == "pygrc.core.errors" and type(exc).__name__ == "InvalidStateTransitionError", f"unexpected native exception: {type(exc).__module__}.{type(exc).__name__}")
        refusal_reason = str(exc)
        require(refusal_reason == "source coherence is smaller than packet amount", "unexpected native refusal reason")
        require(native_identity_digest(model) == scheduled_identity, "native refusal was not atomic at scheduled boundary")
        disposition = "field_limited_refusal"
    return {
        "parent_checkpoint": checkpoint_bundle,
        "participant_class": case["participant_class"],
        "route_role": case["route_role"],
        "selected_route": selected,
        "carrier_pre": carrier_pre,
        "q_probe": q_probe,
        "signed_admissibility_margin": carrier_pre - q_probe,
        "native_disposition": disposition,
        "refusal_reason": refusal_reason,
        "request": packet,
        "receipts": receipts,
        "native_identity_before_schedule": before_identity,
        "native_identity_at_pre_step_boundary": scheduled_identity,
        "native_identity_terminal": native_identity_digest(model),
        "distance_annotations": distance_annotations(model, source),
        "audit": {
            "field_state_read_by_request_constructor": False,
            "participant_tag_read_by_request_constructor": False,
            "raw_id_read_as_scientific_selector": False,
            "fresh_nondepositor_changes_request": False,
        },
        "source_components": components,
    }


def execute_integrity_fault(
    *,
    registration: Mapping[str, Any],
    matrix: Mapping[str, Any],
    case: Mapping[str, Any],
    configuration: Mapping[str, Any],
    content_store: Path,
    prepared_model: LGRC9V3,
    prepared_baseline_identity: str,
) -> dict[str, Any]:
    topology = topology_for(registration, int(configuration["realization_id"]))
    model = prepared_model
    baseline_identity = prepared_baseline_identity
    before = native_identity_digest(model)
    require(before == baseline_identity, "integrity case operational baseline identity drifted")
    bundle = write_checkpoint_bundle(
        model=model,
        content_store=content_store,
        checkpoint_id=f"{case['case_id']}:valid-parent",
        policy_state=initial_policy_state(policy_binding(topology, "A", float(delay))),
        execution_state={"configuration_id": configuration["configuration_id"], "checkpoint": "integrity-parent"},
        measurement_state={"probe_executed": False},
        reset_state={"baseline_native_restoration_v2_digest": before},
        audit_state={"integrity_parent": True},
    )
    invalid = deepcopy(bundle["manifest"])
    fault = case["fault_type"]
    if fault == "invalid_load":
        invalid["components"]["native.json"]["sha256"] = "0" * 64
    elif fault == "invalid_reset":
        invalid["components"]["reset.json"]["sha256"] = "1" * 64
    elif fault == "invalid_branch":
        invalid["checkpoint_id"] = "wrong-branch"
    elif fault == "invalid_continuation":
        invalid["unknown_continuation_field"] = True
    else:
        raise RuntimeError(f"unknown integrity fault: {fault}")
    refused = False
    reason = None
    try:
        load_checkpoint_bundle(content_store=content_store, manifest=invalid)
    except Exception as exc:
        refused = True
        reason = str(exc)
    require(refused, "invalid composite request was admitted")
    require(native_identity_digest(model) == before, "integrity refusal changed source native state")
    return {
        "fault_type": fault,
        "refused": True,
        "refusal_reason": reason,
        "native_identity_before": before,
        "native_identity_after": native_identity_digest(model),
        "scientific_evidence_effect": "none",
        "scientific_continuation": False,
    }


def validate_claim(*, entry: Mapping[str, Any], claim: Mapping[str, Any], expected_head: str) -> None:
    require(claim["artifact_id"] == "P2-I3-BR-C01-ENTRY-ATTEMPT-CLAIM", "wrong entry claim")
    require(claim["entry_id"] == entry["entry_id"], "entry claim identity drift")
    require(claim["case_id"] == entry["case_id"], "case claim identity drift")
    require(claim["launch_head"] == expected_head, "launch HEAD claim drift")
    require(claim["entry_operation_identity"] == payload_digest({"entry": entry}), "entry claim operation identity drift")


def validate_authorization(
    *, entry: Mapping[str, Any], claim: Mapping[str, Any], p5: Mapping[str, Any], expected_head: str
) -> None:
    validate_claim(entry=entry, claim=claim, expected_head=expected_head)
    require(p5["artifact_id"] == "P2-I3-BR-C01-P5-AUTHORIZATION", "wrong P5 record")
    require(claim["entry_id"] == p5["entry_id"] == entry["entry_id"], "entry authorization identity drift")
    require(claim["case_id"] == p5["case_id"] == entry["case_id"], "case authorization identity drift")
    require(claim["attempt"] == p5["attempt"], "attempt authorization drift")
    require(claim["launch_head"] == p5["launch_head"] == expected_head, "launch HEAD authorization drift")
    require(p5["dispatch_authorized"] is True and p5["single_use"] is True, "P5 does not authorize one dispatch")
    require(p5["entry_operation_identity"] == payload_digest({"entry": entry}), "P5 entry operation identity drift")


def prepare_entry(
    *,
    registration: Mapping[str, Any],
    matrix: Mapping[str, Any],
    entry: Mapping[str, Any],
    content_store: Path,
) -> dict[str, Any]:
    if entry["entry_kind"] == "operational_baseline_construction":
        return {
            "kind": "operational_baseline_construction",
            "model": None,
            "preparation_identity": payload_digest(
                {
                    "entry_id": entry["entry_id"],
                    "realization_id": entry["realization_id"],
                    "delay_profile_id": entry["delay_profile_id"],
                    "operation": "validated_unexecuted_baseline_construction",
                }
            ),
        }
    if entry["branch_kind"] in {"terminal_probe", "fresh_nondepositor_terminal_probe"}:
        parent = parent_trajectory_row(matrix, entry)
        parent_manifest_path = ROOT / parent["governed_paths"]["logical_manifest"]
        parent_result = load_json(parent_manifest_path)
        checkpoint = str(entry["checkpoint"])
        checkpoint_bundle = parent_result["result"]["checkpoints"][checkpoint]
        model, components = load_checkpoint_bundle(
            content_store=content_store,
            manifest=checkpoint_bundle["manifest"],
        )
        return {
            "kind": "terminal_probe",
            "model": model,
            "components": components,
            "checkpoint_bundle": checkpoint_bundle,
            "preparation_identity": checkpoint_bundle["exact_composite_identity"],
        }
    model, baseline_identity, components = load_operational_baseline(
        matrix=matrix,
        entry=entry,
        content_store=content_store,
    )
    return {
        "kind": entry["case_kind"],
        "model": model,
        "components": components,
        "baseline_identity": baseline_identity,
        "preparation_identity": baseline_identity,
    }


def wait_for_p5(path: Path, *, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if path.is_file():
            return load_json(path)
        time.sleep(0.01)
    raise RuntimeError("supervisor P5 authorization was not issued before child wait deadline")


def retain_child_failure(
    *,
    path: Path,
    entry: Mapping[str, Any],
    claim: Mapping[str, Any],
    stage: str,
    p5_observed: bool,
    exc: Exception,
) -> None:
    infrastructure = isinstance(exc, (OSError, TimeoutError))
    if p5_observed and infrastructure:
        hint = "post_candidate_infrastructure_failure"
    elif not p5_observed and infrastructure:
        hint = "attested_pre_candidate_infrastructure_failure"
    else:
        hint = "invalid_execution"
    write_exclusive_json(
        path,
        with_digest(
            {
                "artifact_id": "P2-I3-BR-C01-CHILD-FAILURE",
                "artifact_version": "1.0.0",
                "entry_id": entry["entry_id"],
                "case_id": entry["case_id"],
                "attempt": claim["attempt"],
                "claim_digest": claim["canonical_payload_digest"],
                "stage": stage,
                "p5_observed": p5_observed,
                "status_hint": hint,
                "exception_module": type(exc).__module__,
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "scientific_interpretation_assigned": False,
            }
        ),
    )


def command_run_case(args: argparse.Namespace) -> int:
    registration = load_json(ROOT / REGISTRATION_REL)
    matrix = load_json(ROOT / MATRIX_REL)
    freeze = load_json(ROOT / FREEZE_REL)
    policy = load_json(ROOT / POLICY_REL)
    verify_digest(registration)
    verify_digest(matrix)
    verify_digest(freeze)
    require(
        freeze["matrix"]["sha256"] == sha256_file(ROOT / MATRIX_REL),
        "freeze/run-matrix byte binding drifted",
    )
    require(freeze["gate_effect"]["candidate_execution"] is False, "inactive freeze shape drifted")
    matches = [row for row in matrix["entries"] if row["entry_id"] == args.entry_id]
    require(len(matches) == 1, "entry is not in frozen matrix")
    entry = matches[0]
    claim = load_json(Path(args.claim).resolve())
    verify_digest(claim)
    campaign_claim = load_json(ROOT / policy["live_paths"]["campaign_claim"])
    verify_digest(campaign_claim)
    require(
        claim["campaign_claim_digest"] == campaign_claim["canonical_payload_digest"],
        "entry claim campaign binding drifted",
    )
    validate_claim(entry=entry, claim=claim, expected_head=args.expected_head)
    configurations = {row["configuration_id"]: row for row in registration["matrix"]["configurations"]}
    governed_root = Path(args.governed_root).resolve()
    graph_root_raw = os.environ.get(policy["environment"]["graph_root_environment_variable"])
    require(bool(graph_root_raw), "machine-local graph root is absent")
    graph_source = (Path(str(graph_root_raw)).resolve() / "src").resolve()
    require(
        Path(pygrc.__file__).resolve() == graph_source / "pygrc" / "__init__.py",
        "child PyGRC import escaped the exact admitted source root",
    )
    content_store = governed_root / "content" / "sha256"
    content_store.mkdir(parents=True, exist_ok=True)
    failure_path = Path(args.failure).resolve()
    try:
        prepared = prepare_entry(
            registration=registration,
            matrix=matrix,
            entry=entry,
            content_store=content_store,
        )
    except Exception as exc:
        retain_child_failure(
            path=failure_path,
            entry=entry,
            claim=claim,
            stage="preparation_before_P5",
            p5_observed=False,
            exc=exc,
        )
        raise
    ready = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-ENTRY-P4-READY",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "case_id": entry["case_id"],
            "attempt": claim["attempt"],
            "claim_digest": claim["canonical_payload_digest"],
            "preparation_identity": prepared["preparation_identity"],
            "parent_restored_and_validated": entry["entry_kind"] != "operational_baseline_construction",
            "baseline_construction_not_started": entry["entry_kind"] == "operational_baseline_construction",
            "p5_observed": False,
            "scientific_or_integrity_operation_count": 0,
        }
    )
    write_exclusive_json(Path(args.ready).resolve(), ready)
    try:
        p5 = wait_for_p5(Path(args.p5).resolve(), timeout_seconds=float(args.p5_wait_seconds))
        validate_authorization(entry=entry, claim=claim, p5=p5, expected_head=args.expected_head)
        p5_consumption = with_digest(
            {
                "artifact_id": "P2-I3-BR-C01-P5-CONSUMPTION",
                "artifact_version": "1.0.0",
                "entry_id": entry["entry_id"],
                "case_id": entry["case_id"],
                "attempt": claim["attempt"],
                "claim_digest": claim["canonical_payload_digest"],
                "p5_digest": p5["canonical_payload_digest"],
                "entry_operation_identity": payload_digest({"entry": entry}),
                "consumed_once": True,
            }
        )
        write_exclusive_json(Path(args.p5_consumption).resolve(), p5_consumption)
        if entry["entry_kind"] == "operational_baseline_construction":
            result = execute_operational_baseline(
                registration=registration,
                matrix=matrix,
                entry=entry,
                content_store=content_store,
            )
        else:
            configuration = configurations[entry["configuration_id"]]
            if entry["case_kind"] == "quarantined_integrity_fault":
                result = execute_integrity_fault(registration=registration, matrix=matrix, case=entry, configuration=configuration, content_store=content_store, prepared_model=prepared["model"], prepared_baseline_identity=prepared["baseline_identity"])
            elif entry["branch_kind"] in {"terminal_probe", "fresh_nondepositor_terminal_probe"}:
                result = execute_probe(registration=registration, matrix=matrix, case=entry, configuration=configuration, governed_root=governed_root, content_store=content_store, prepared_model=prepared["model"], prepared_components=prepared["components"], prepared_checkpoint_bundle=prepared["checkpoint_bundle"])
            elif entry["branch_kind"] == "unprobed_trajectory":
                result = execute_trajectory(registration=registration, matrix=matrix, entry=entry, configuration=configuration, content_store=content_store, prepared_model=prepared["model"], prepared_baseline_identity=prepared["baseline_identity"])
            else:
                raise RuntimeError("unregistered entry dispatch")
    except Exception as exc:
        if not failure_path.exists():
            retain_child_failure(
                path=failure_path,
                entry=entry,
                claim=claim,
                stage="dispatch_at_or_after_P5",
                p5_observed=Path(args.p5).is_file(),
                exc=exc,
            )
        raise
    record = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-ENTRY-LOGICAL-MANIFEST",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "entry_kind": entry["entry_kind"],
            "case_id": entry["case_id"],
            "attempt": claim["attempt"],
            "launch_head": args.expected_head,
            "entry_operation_identity": payload_digest({"entry": entry}),
            "result": result,
            "scientific_interpretation_assigned": False,
            "control_outcome_assigned": False,
            "rung_or_tag_assigned": False,
        }
    )
    output = Path(args.output).resolve()
    require(not output.exists(), "case logical manifest already exists")
    write_exclusive_json(output, record)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run-entry")
    run.add_argument("--entry-id", required=True)
    run.add_argument("--claim", required=True)
    run.add_argument("--ready", required=True)
    run.add_argument("--failure", required=True)
    run.add_argument("--p5", required=True)
    run.add_argument("--p5-consumption", required=True)
    run.add_argument("--p5-wait-seconds", required=True, type=float)
    run.add_argument("--expected-head", required=True)
    run.add_argument("--governed-root", required=True)
    run.add_argument("--output", required=True)
    run.set_defaults(func=command_run_case)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
