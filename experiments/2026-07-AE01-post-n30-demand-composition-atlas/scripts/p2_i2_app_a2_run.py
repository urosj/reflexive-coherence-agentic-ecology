#!/usr/bin/env python3
"""Execute the single frozen P2-I2 APP-A2 fresh-process campaign."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any, Mapping, Sequence

import pygrc
from pygrc.core import PortGraphBackend
from pygrc.models import (
    CAUSAL_LAYER_MODE_PACKETIZED_FIXED_TOPOLOGY,
    EDGE_DELAY_POLICY_CONSTANT_DELAY,
    GRC9V3NodeState,
    GRC9V3State,
    LAPSE_POLICY_UNIT,
    LGRC_RUNTIME_LEVEL_LGRC2,
    LGRC9V3,
    LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FLUX_ROUTE,
    LGRC9V3_AUTONOMOUS_PRODUCER_REASON_PACKET_DEPARTURE_SCHEDULED,
    PortEdge,
    build_lgrc9v3_packet_ledger,
    digest_lgrc9v3_restoration_identity_v2,
)

from p2_i2_app_a2_analysis import AXES, analyze_receipts, canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"
GRAPH_SOURCE_ROOT = GRAPH_ROOT / "src"
SCRIPT_REL = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_app_a2_run.py"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def portable_failure_message(exc: Exception) -> str:
    """Keep failed-closed evidence free of checkout-specific absolute paths."""

    message = str(exc)
    replacements = (
        (str(GRAPH_SOURCE_ROOT), "external-repository:graph-reflexive-coherence/src"),
        (str(GRAPH_ROOT), "external-repository:graph-reflexive-coherence"),
        (str(ROOT), "repository-root"),
        (tempfile.gettempdir(), "temporary-root"),
    )
    for absolute, logical in replacements:
        message = message.replace(absolute, logical)
    return message


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def resolve_root_path(value: str) -> Path:
    path = Path(value)
    require(not path.is_absolute(), "absolute paths prohibited")
    return ROOT / path


def validate_implementation_hashes(freeze: Mapping[str, Any]) -> None:
    for row in freeze["implementation_files"]:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing implementation file: {row['path']}")
        require(sha256_file(path) == row["sha256"], f"implementation hash mismatch: {row['path']}")


def validate_static_validation(freeze: Mapping[str, Any], freeze_path: Path) -> None:
    validation_path = ROOT / freeze["static_validation_policy"]["output"]
    require(validation_path.is_file(), "inactive static validation missing")
    validation = load_json(validation_path)
    require(
        validation["artifact_id"] == "p2_i2_app_a2_inactive_static_validation",
        "wrong inactive static validation",
    )
    require(validation["status"] == "passed", "inactive static validation failed")
    require(validation["checks_passed"] == validation["checks_total"], "inactive checks incomplete")
    require(not validation["failed_checks"], "inactive validation retains failures")
    require(
        validation["activation_freeze"]["sha256"] == sha256_file(freeze_path),
        "inactive validation freeze identity drift",
    )
    unsigned = dict(validation)
    observed_digest = unsigned.pop("output_digest")
    require(digest_value(unsigned) == observed_digest, "inactive validation digest drift")
    require(
        all(value == 0 for value in validation["zero_science_receipt"].values()),
        "inactive validation crossed scientific boundary",
    )


def validate_runtime_authority(
    authorization_path: Path,
    *,
    worker: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    authorization = load_json(authorization_path)
    require(
        authorization["artifact_id"]
        == "P2-I2-APP-A2-ACTIVATION-AUTHORIZATION",
        "wrong activation authorization",
    )
    require(authorization["status"] == "active_for_single_campaign", "activation inactive")
    authority = authorization["authority"]
    require(authority["campaign_authorized"] is True, "campaign unauthorized")
    require(authority["owner_acceptance"] is True, "owner acceptance absent")
    require(authority["campaign_invocations"] == 1, "wrong campaign count")
    require(authority["campaign_retry_limit"] == 0, "campaign retry opened")
    require(authority["attempts_per_arm"] == 1, "wrong arm attempt count")
    require(authority["arm_retry_limit"] == 0, "arm retry opened")

    freeze_ref = authorization["activation_freeze"]
    freeze_path = ROOT / freeze_ref["path"]
    require(freeze_path.is_file(), "activation freeze missing")
    require(sha256_file(freeze_path) == freeze_ref["sha256"], "activation freeze hash mismatch")
    freeze = load_json(freeze_path)
    require(
        freeze["artifact_id"] == "P2-I2-APP-A2-INACTIVE-ACTIVATION-FREEZE",
        "wrong activation freeze",
    )
    require(freeze["status"] == "validated_inactive_pending_owner_activation", "freeze not validated inactive")
    expected_authorization = ROOT / freeze["future_activation_authorization"]["path"]
    require(authorization_path == expected_authorization.resolve(), "authorization path drift")
    require(
        authority["normalized_campaign_command"]
        == freeze["normalized_commands"]["campaign"],
        "campaign command identity drift",
    )
    require(
        authority["normalized_worker_command"]
        == freeze["normalized_commands"]["worker"],
        "worker command identity drift",
    )
    require(
        authority["normalized_reconstruction_command"]
        == freeze["normalized_commands"]["reconstruction"],
        "reconstruction command identity drift",
    )
    validate_implementation_hashes(freeze)
    validate_static_validation(freeze, freeze_path)

    authorization_rel = str(authorization_path.relative_to(ROOT))
    tracked = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{authorization_rel}"],
        cwd=ROOT,
        capture_output=True,
    ).returncode == 0
    require(tracked, "activation authorization is not retained in HEAD")
    committed_authorization = subprocess.run(
        ["git", "show", f"HEAD:{authorization_rel}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    require(
        hashlib.sha256(committed_authorization).hexdigest()
        == sha256_file(authorization_path),
        "local activation authorization differs from HEAD",
    )
    implementation_commit = authority["implementation_commit"]
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", implementation_commit, "HEAD"],
            cwd=ROOT,
        ).returncode
        == 0,
        "implementation commit is not an ancestor of HEAD",
    )

    require(git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == freeze["graph"]["commit"], "graph commit drift")
    require(git("status", "--short", cwd=GRAPH_ROOT) == "", "graph checkout dirty")
    for row in freeze["graph"]["source_identities"]:
        path = GRAPH_ROOT / row["path"]
        require(sha256_file(path) == row["sha256"], f"graph source drift: {row['path']}")

    require(Path(sys.executable).resolve() == (ROOT / ".venv" / "bin" / "python").resolve(), "repository venv inactive")
    require(platform.python_version() == freeze["environment"]["python_version"], "Python version drift")
    require(sha256_file(ROOT / ".venv" / "bin" / "python") == freeze["environment"]["interpreter_sha256"], "interpreter drift")
    expected_import = (GRAPH_SOURCE_ROOT / "pygrc" / "__init__.py").resolve()
    require(Path(pygrc.__file__).resolve() == expected_import, "wrong PyGRC import")
    require(any(Path(row).resolve() == GRAPH_SOURCE_ROOT.resolve() for row in sys.path if row), "checkout source binding absent")
    versions = {
        package: importlib.metadata.version(package)
        for package in freeze["environment"]["direct_dependencies"]
    }
    require(versions == freeze["environment"]["direct_dependencies"], "dependency drift")

    execution_ref = freeze["retained_app_a1"]["execution_freeze"]
    execution_path = ROOT / execution_ref["path"]
    require(sha256_file(execution_path) == execution_ref["sha256"], "APP-A1 execution freeze drift")
    execution = load_json(execution_path)
    fixture_ref = freeze["retained_app_a1"]["fixture_freeze"]
    fixture_path = ROOT / fixture_ref["path"]
    require(sha256_file(fixture_path) == fixture_ref["sha256"], "APP-A1 fixture freeze drift")
    fixture = load_json(fixture_path)
    expected_arm_ids = execution["frozen_registry_import"]["arm_order"]
    actual_arm_ids = [row["arm_id"] for row in fixture["arm_registry"]]
    require(actual_arm_ids == expected_arm_ids, "frozen arm order drift")
    campaign_policy = execution["campaign_policy"]
    require(len(actual_arm_ids) == campaign_policy["arm_count"] == 19, "arm count drift")
    require(campaign_policy["campaign_invocations"] == 1, "campaign invocation drift")
    require(campaign_policy["campaign_retry_limit"] == 0, "campaign retry drift")
    require(campaign_policy["attempts_per_arm"] == 1, "arm attempt drift")
    require(campaign_policy["arm_retry_limit"] == 0, "arm retry drift")

    output_path = ROOT / execution["campaign_policy"]["single_aggregate_persisted_output"]
    status_rows = [row for row in git("status", "--short").splitlines() if row]
    if worker:
        allowed = {f"?? {output_path.relative_to(ROOT)}"}
        require(set(status_rows).issubset(allowed), f"worker authority tree dirty: {status_rows}")
    else:
        require(not status_rows, f"campaign authority tree dirty: {status_rows}")
        require(not output_path.exists(), "governed aggregate already exists")
        reconstruction_path = ROOT / execution["campaign_policy"]["read_only_reconstruction_output"]
        require(not reconstruction_path.exists(), "reconstruction output already exists")

    return authorization, freeze, {"execution": execution, "fixture": fixture}


def build_model(
    fixture: Mapping[str, Any],
    arm: Mapping[str, Any],
) -> tuple[LGRC9V3, dict[str, int], dict[str, int]]:
    topology = fixture["topology"]
    graph = PortGraphBackend()
    label_overrides = (
        fixture["scientific_fixture"]["label_permutation"]
        if arm["labels"] == "label_permutation"
        else {}
    )
    role_ids: dict[str, int] = {}
    for node in topology["nodes"]:
        role = str(node["role"])
        node_id = graph.add_node({"label": label_overrides.get(role, role)})
        require(node_id == int(node["node_id"]), f"node id drift: {role}")
        role_ids[role] = node_id

    next_slot = {node_id: 0 for node_id in role_ids.values()}
    edge_ids: dict[str, int] = {}
    port_edges: dict[int, PortEdge] = {}
    for edge in topology["edges"]:
        left = role_ids[str(edge["left"])]
        right = role_ids[str(edge["right"])]
        left_slot = next_slot[left]
        right_slot = next_slot[right]
        edge_id = graph.connect_ports(
            left,
            left_slot,
            right,
            right_slot,
            {"kind": str(edge["edge_role"])},
        )
        require(edge_id == int(edge["edge_id"]), f"edge id drift: {edge['edge_role']}")
        next_slot[left] += 1
        next_slot[right] += 1
        edge_ids[str(edge["edge_role"])] = edge_id
        port_edges[edge_id] = PortEdge(
            left,
            left_slot + 1,
            right,
            right_slot + 1,
            conductance=1.0,
            flux_uv=0.0,
        )

    initial = dict(fixture["scientific_fixture"]["initial_coherence"])
    if arm.get("initial_override") == "one_source_capacity_override":
        initial.update(fixture["scientific_fixture"]["one_source_capacity_override"])
    node_states = {
        role_ids[role]: GRC9V3NodeState(coherence=float(initial[role]))
        for role in role_ids
    }
    ones = {edge_id: 1.0 for edge_id in edge_ids.values()}
    zeros = {edge_id: 0.0 for edge_id in edge_ids.values()}
    state = GRC9V3State(
        topology=graph,
        nodes=node_states,
        port_edges=port_edges,
        base_conductance=ones,
        geometric_length=ones,
        temporal_delay=ones,
        flux_coupling=zeros,
    )
    params = {
        "dt": 1.0,
        "causal_modes": {
            "causal_layer_mode": CAUSAL_LAYER_MODE_PACKETIZED_FIXED_TOPOLOGY,
            "lgrc_runtime_level": LGRC_RUNTIME_LEVEL_LGRC2,
            "lapse_policy": LAPSE_POLICY_UNIT,
            "edge_delay_policy": EDGE_DELAY_POLICY_CONSTANT_DELAY,
            "event_time_policy": "explicit_event_time_key",
            "proper_time_accumulation_policy": "local_event_frontier",
        },
    }
    return LGRC9V3.from_state(state, params), role_ids, edge_ids


def coherences(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, float]:
    nodes = model.get_state().base_state.nodes
    return {role: float(nodes[node_id].coherence) for role, node_id in role_ids.items()}


def carrier_vector(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, float]:
    values = coherences(model, role_ids)
    return {axis: values[f"c_{axis}"] for axis in AXES}


def event_receipt(result: Any) -> dict[str, Any]:
    budget_errors = [
        float(event.payload["budget_error"])
        for event in result.events
        if "budget_error" in event.payload
    ]
    return {
        "event_kind": result.bookkeeping["processed_event_kind"],
        "event_id": result.bookkeeping["processed_event_id"],
        "budget_error": max(budget_errors, key=abs) if budget_errors else 0.0,
    }


def transfer(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    *,
    arm_id: str,
    operation: str,
    source: str,
    target: str,
    amount: float,
    pair_index: int,
) -> dict[str, Any]:
    edge_role = "__".join(sorted((source, target)))
    departure = float(2 * pair_index + 1)
    arrival = float(2 * pair_index + 2)
    before = coherences(model, role_ids)
    old_packet_ids = {
        row.packet_id for row in model.get_state().packet_ledger.packet_records
    }
    model.schedule_packet_departure(
        source_node_id=role_ids[source],
        target_node_id=role_ids[target],
        edge_id=edge_ids[edge_role],
        amount=float(amount),
        departure_event_time_key=departure,
        arrival_event_time_key=arrival,
        scheduler_event_index=int(2 * pair_index + 1),
        packet_index=pair_index,
        source_lineage_id=f"app-a2:{arm_id}:{operation}:{source}",
        target_lineage_id=f"app-a2:{arm_id}:{operation}:{target}",
    )
    queue_after_schedule = len(model.get_state().packet_ledger.event_queue_records)
    results = [model.step(), model.step()]
    after = coherences(model, role_ids)
    new_packets = [
        row
        for row in model.get_state().packet_ledger.packet_records
        if row.packet_id not in old_packet_ids
    ]
    require(len(new_packets) == 1, "operation packet count drift")
    return {
        "source_role": source,
        "target_role": target,
        "edge_role": edge_role,
        "amount": float(amount),
        "pair_index": pair_index,
        "packet_index": pair_index,
        "departure_event_time_key": departure,
        "arrival_event_time_key": arrival,
        "source_delta": after[source] - before[source],
        "target_delta": after[target] - before[target],
        "queue_length_after_schedule": queue_after_schedule,
        "processed_events": [event_receipt(result) for result in results],
        "packet_record": new_packets[0].to_record(),
    }


def run_operation(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    fixture: Mapping[str, Any],
    arm: Mapping[str, Any],
    *,
    operation: str,
    position: int,
) -> dict[str, Any]:
    scientific = fixture["scientific_fixture"]
    actors = scientific["actor_assignments"][arm["actors"]]
    actor = str(actors[operation])
    selected = operation in set(arm["common_operations"])
    prefix = "c" if selected else "d"
    vectors = scientific["operation_vectors"]
    before_carrier = carrier_vector(model, role_ids)
    input_identity = digest_lgrc9v3_restoration_identity_v2(model)
    transfers: list[dict[str, Any]] = []
    base_pair = position * 4
    if operation == "G":
        for index, axis in enumerate(AXES):
            transfers.append(
                transfer(
                    model,
                    role_ids,
                    edge_ids,
                    arm_id=str(arm["arm_id"]),
                    operation=operation,
                    source=actor,
                    target=f"{prefix}_{axis}",
                    amount=float(vectors["G"][axis]),
                    pair_index=base_pair + index,
                )
            )
    elif operation == "E":
        for index, axis in enumerate(AXES):
            transfers.append(
                transfer(
                    model,
                    role_ids,
                    edge_ids,
                    arm_id=str(arm["arm_id"]),
                    operation=operation,
                    source=f"{prefix}_{axis}",
                    target=actor,
                    amount=float(vectors["E"][axis]),
                    pair_index=base_pair + index,
                )
            )
    elif operation == "P":
        transfers.append(
            transfer(
                model,
                role_ids,
                edge_ids,
                arm_id=str(arm["arm_id"]),
                operation=operation,
                source=f"{prefix}_boundary",
                target=actor,
                amount=float(vectors["P"]["boundary_out"]),
                pair_index=base_pair,
            )
        )
        for index, axis in enumerate(("environment", "support", "distinguishability"), start=1):
            transfers.append(
                transfer(
                    model,
                    role_ids,
                    edge_ids,
                    arm_id=str(arm["arm_id"]),
                    operation=operation,
                    source=actor,
                    target=f"{prefix}_{axis}",
                    amount=float(vectors["P"][axis]),
                    pair_index=base_pair + index,
                )
            )
    else:
        raise AssertionError(f"unknown operation: {operation}")
    return {
        "operation": operation,
        "position": position,
        "actor_role": actor,
        "selected_common": selected,
        "route_namespace": "common" if selected else "diversion",
        "input_identity": input_identity,
        "output_identity": digest_lgrc9v3_restoration_identity_v2(model),
        "before_carrier": before_carrier,
        "after_carrier": carrier_vector(model, role_ids),
        "cost_proxy": sum(float(row["amount"]) for row in transfers),
        "transfers": transfers,
    }


def rebase_packet_ledger_after_intervention(state: Any) -> dict[str, Any]:
    old = state.packet_ledger
    require(old is not None, "packet ledger absent")
    require(not old.event_queue_records, "intervention queue not empty")
    state.packet_ledger = build_lgrc9v3_packet_ledger(
        packet_records=old.packet_records,
        packet_event_records=old.packet_event_records,
        event_queue_records=old.event_queue_records,
        state=state.base_state,
        policies=old.policies,
        causal_layer_mode=old.causal_layer_mode,
        lgrc_runtime_level=old.lgrc_runtime_level,
        evidence_class=old.evidence_class,
        fixed_topology=old.fixed_topology,
        topology_change_allowed=old.topology_change_allowed,
        packet_transport_through_topology_change=old.packet_transport_through_topology_change,
        identity_acceptance_allowed=old.identity_acceptance_allowed,
        collapse_allowed=old.collapse_allowed,
    )
    rebased = state.packet_ledger
    return {
        "mechanism": "pygrc.models.build_lgrc9v3_packet_ledger",
        "packet_history_preserved": rebased.packet_records == old.packet_records,
        "packet_event_history_preserved": rebased.packet_event_records == old.packet_event_records,
        "queue_was_empty": not old.event_queue_records,
        "old_node_coherence_total": float(old.node_coherence_total),
        "new_node_coherence_total": float(rebased.node_coherence_total),
        "old_conserved_budget_total": float(old.conserved_budget_total),
        "new_conserved_budget_total": float(rebased.conserved_budget_total),
        "new_budget_error": float(rebased.budget_error),
    }


def apply_intervention(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    arm: Mapping[str, Any],
    execution: Mapping[str, Any],
) -> dict[str, Any] | None:
    kind = str(arm["intervention"])
    if kind == "none":
        return None
    targets = execution["frozen_registry_import"]["registered_intervention_targets"]
    if kind == "clamp_all_carrier_axes_to_matched_reference_pre_r":
        target = targets["matched_reference_pre_r"]
    elif kind == "restore_all_carrier_axes_to_registered_GEP_pre_r":
        target = targets["registered_GEP_pre_r"]
    else:
        raise AssertionError(f"unknown intervention: {kind}")
    state = deepcopy(model.get_state())
    identity_before = digest_lgrc9v3_restoration_identity_v2(model)
    before = carrier_vector(model, role_ids)
    for axis in AXES:
        state.base_state.nodes[role_ids[f"c_{axis}"]].coherence = float(target[axis])
    rebase = rebase_packet_ledger_after_intervention(state)
    model.set_state(state)
    return {
        "kind": kind,
        "state_setter": "public LGRC9V3.set_state",
        "target_carrier": {axis: float(target[axis]) for axis in AXES},
        "target_carrier_total": sum(float(target[axis]) for axis in AXES),
        "before_carrier": before,
        "after_carrier": carrier_vector(model, role_ids),
        "identity_before": identity_before,
        "identity_after": digest_lgrc9v3_restoration_identity_v2(model),
        "packet_ledger_rebase": rebase,
    }


def produce_response(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    fraction = float(fixture["measurement_authority"]["retention_fraction"])
    pre_identity = digest_lgrc9v3_restoration_identity_v2(model)
    pre_coherence = coherences(model, role_ids)
    old_packet_ids = {row.packet_id for row in model.get_state().packet_ledger.packet_records}
    routes = {
        role_ids[f"c_{axis}"]: [
            {
                "target_node_id": role_ids["r"],
                "edge_id": edge_ids["__".join(sorted((f"c_{axis}", "r")))],
                "amount_fraction": fraction,
            }
        ]
        for axis in AXES
    }
    model.set_causal_flux_routes(routes)
    production = model.produce_events(
        policy=LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FLUX_ROUTE
    )
    records = list(production.production_records)
    require(len(records) == 4, "response production count drift")
    require(
        all(
            row.reason_code
            == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_PACKET_DEPARTURE_SCHEDULED
            for row in records
        ),
        "response production refused",
    )
    queue_after_production = len(model.get_state().packet_ledger.event_queue_records)
    steps = model.run_event_queue(max_events=8)
    require(len(steps) == 8, "response event count drift")
    ledger = model.get_state().packet_ledger
    new_packets = [row for row in ledger.packet_records if row.packet_id not in old_packet_ids]
    require(len(new_packets) == 4, "response packet count drift")
    role_by_id = {node_id: role for role, node_id in role_ids.items()}
    packet_mass_by_axis: dict[str, float] = {}
    unregistered = 0.0
    for packet in new_packets:
        source_role = role_by_id[int(packet.source_node_id)]
        target_role = role_by_id[int(packet.target_node_id)]
        if source_role.startswith("c_") and target_role == "r":
            packet_mass_by_axis[source_role.removeprefix("c_")] = float(packet.amount)
        else:
            unregistered += float(packet.amount)
    post = coherences(model, role_ids)
    return {
        "input_identity": pre_identity,
        "retention_fraction": fraction,
        "pre_r_carrier": {axis: pre_coherence[f"c_{axis}"] for axis in AXES},
        "packet_mass_by_axis": packet_mass_by_axis,
        "r_delta": post["r"] - pre_coherence["r"],
        "producer_policy": production.producer_policy,
        "producer_records": [row.to_artifact() for row in records],
        "packet_records": [row.to_record() for row in new_packets],
        "source_roles": sorted(role_by_id[int(row.source_node_id)] for row in new_packets),
        "target_roles": sorted(role_by_id[int(row.target_node_id)] for row in new_packets),
        "processed_events": [event_receipt(step) for step in steps],
        "queue_length_after_production": queue_after_production,
        "queue_empty_after": not ledger.event_queue_records,
        "unregistered_shared_carrier_packet_mass": unregistered,
        "post_r_carrier": {axis: post[f"c_{axis}"] for axis in AXES},
        "output_identity": digest_lgrc9v3_restoration_identity_v2(model),
    }


def restoration_receipt(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
) -> dict[str, Any]:
    before_save = digest_lgrc9v3_restoration_identity_v2(model)
    with tempfile.TemporaryDirectory(prefix="p2-i2-app-a2-") as directory:
        path = Path(directory) / "snapshot.json"
        model.save(str(path))
        loaded = LGRC9V3.load(str(path))
    after_load = digest_lgrc9v3_restoration_identity_v2(loaded)
    model.step()
    loaded.step()
    original_after_empty = digest_lgrc9v3_restoration_identity_v2(model)
    loaded_after_empty = digest_lgrc9v3_restoration_identity_v2(loaded)
    model.reset()
    loaded.reset()
    return {
        "identity_before_save": before_save,
        "identity_after_load": after_load,
        "original_after_empty_step": original_after_empty,
        "loaded_after_empty_step": loaded_after_empty,
        "original_after_reset": digest_lgrc9v3_restoration_identity_v2(model),
        "loaded_after_reset": digest_lgrc9v3_restoration_identity_v2(loaded),
        "loaded_post_reset_coherence": coherences(loaded, role_ids),
    }


def run_arm(
    arm: Mapping[str, Any],
    fixture: Mapping[str, Any],
    execution: Mapping[str, Any],
) -> dict[str, Any]:
    model, role_ids, edge_ids = build_model(fixture, arm)
    baseline_identity = digest_lgrc9v3_restoration_identity_v2(model)
    baseline_coherence = coherences(model, role_ids)
    operation_receipts = [
        run_operation(
            model,
            role_ids,
            edge_ids,
            fixture,
            arm,
            operation=str(operation),
            position=position,
        )
        for position, operation in enumerate(arm["sequence"])
    ]
    pre_intervention = {
        "identity": digest_lgrc9v3_restoration_identity_v2(model),
        "carrier": carrier_vector(model, role_ids),
    }
    intervention = apply_intervention(model, role_ids, arm, execution)
    pre_r = {
        "identity": digest_lgrc9v3_restoration_identity_v2(model),
        "carrier": carrier_vector(model, role_ids),
    }
    response = produce_response(model, role_ids, edge_ids, fixture)

    event_budget_errors = [
        abs(float(event["budget_error"]))
        for operation in operation_receipts
        for transfer_row in operation["transfers"]
        for event in transfer_row["processed_events"]
    ] + [abs(float(event["budget_error"])) for event in response["processed_events"]]
    response["max_abs_native_budget_error"] = max(
        event_budget_errors + [abs(float(model.get_state().packet_ledger.budget_error))]
    )
    operation_common_mass = sum(
        float(transfer_row["amount"])
        for operation in operation_receipts
        if operation["selected_common"]
        for transfer_row in operation["transfers"]
    )
    response["total_registered_common_carrier_packet_mass"] = (
        operation_common_mass
        + sum(float(value) for value in response["packet_mass_by_axis"].values())
    )

    final_state = model.get_state()
    queue_lengths = [
        int(transfer_row["queue_length_after_schedule"])
        for operation in operation_receipts
        for transfer_row in operation["transfers"]
    ] + [int(response["queue_length_after_production"])]
    receipt: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a2_arm_runtime_receipt",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-A2",
        "arm_id": arm["arm_id"],
        "arm_row": dict(arm),
        "arm_row_digest": digest_value(arm),
        "process_receipt": {
            "fresh_child_process": True,
            "logical_executable": ".venv/bin/python",
            "python_version": platform.python_version(),
            "pygrc_identity": {
                "repository_id": "graph-reflexive-coherence",
                "path": "src/pygrc/__init__.py",
            },
            "prior_result_input_fields": [],
            "persistent_per_arm_output": False,
        },
        "baseline": {
            "fresh_model": True,
            "identity": baseline_identity,
            "coherence": baseline_coherence,
            "role_node_ids": dict(role_ids),
            "edge_role_ids": dict(edge_ids),
            "node_count": len(tuple(final_state.base_state.topology.iter_live_node_ids())),
            "edge_count": len(tuple(final_state.base_state.topology.iter_live_edge_ids())),
        },
        "operation_receipts": operation_receipts,
        "pre_intervention": pre_intervention,
        "intervention": intervention,
        "pre_r": pre_r,
        "response": response,
        "final": {
            "identity": digest_lgrc9v3_restoration_identity_v2(model),
            "coherence": coherences(model, role_ids),
            "packet_count": len(final_state.packet_ledger.packet_records),
            "packet_event_count": len(final_state.packet_ledger.packet_event_records),
            "queue_length": len(final_state.packet_ledger.event_queue_records),
        },
        "restoration": restoration_receipt(model, role_ids),
        "resource_receipt": {
            "node_count": len(tuple(final_state.base_state.topology.iter_live_node_ids())),
            "edge_count": len(tuple(final_state.base_state.topology.iter_live_edge_ids())),
            "packet_events": len(final_state.packet_ledger.packet_event_records),
            "maximum_queue_length": max(queue_lengths),
            "address_space_limit": "none",
        },
    }
    receipt["arm_receipt_digest"] = digest_value(receipt)
    return receipt


def worker_main(authorization_path: Path) -> int:
    _, _, authorities = validate_runtime_authority(authorization_path, worker=True)
    worker_input = json.loads(sys.stdin.read())
    require(set(worker_input) == {"arm"}, "worker input must contain only one arm row")
    arm = worker_input["arm"]
    require(isinstance(arm, dict), "worker arm must be an object")
    frozen_rows = {
        row["arm_id"]: row for row in authorities["fixture"]["arm_registry"]
    }
    require(arm.get("arm_id") in frozen_rows, "unknown arm")
    require(arm == frozen_rows[arm["arm_id"]], "arm row differs from freeze")
    receipt = run_arm(arm, authorities["fixture"], authorities["execution"])
    sys.stdout.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


def write_fd(fd: int, value: Any) -> None:
    data = canonical_bytes(value)
    os.lseek(fd, 0, os.SEEK_SET)
    os.ftruncate(fd, 0)
    written = 0
    while written < len(data):
        written += os.write(fd, data[written:])
    os.fsync(fd)


def campaign_main(authorization_path: Path, output_arg: str) -> int:
    authorization, activation_freeze, authorities = validate_runtime_authority(
        authorization_path,
        worker=False,
    )
    execution = authorities["execution"]
    fixture = authorities["fixture"]
    expected_output = ROOT / execution["campaign_policy"]["single_aggregate_persisted_output"]
    output_path = resolve_root_path(output_arg)
    require(output_path.resolve() == expected_output.resolve(), "output path differs from freeze")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(output_path, flags, 0o644)
    claim = {
        "artifact_id": "p2_i2_app_a2_runtime_evidence",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-A2",
        "status": "campaign_claimed_incomplete",
        "attempt_consumed": True,
        "authorization_sha256": sha256_file(authorization_path),
        "activation_freeze_sha256": authorization["activation_freeze"]["sha256"],
        "app_a2_arm_starts": 0,
        "scientific_result_assigned": False,
    }
    write_fd(fd, claim)
    receipts: list[dict[str, Any]] = []
    child_invocations: list[dict[str, Any]] = []
    try:
        child_env = dict(os.environ)
        child_env.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
                "PYTHONPATH": str(GRAPH_SOURCE_ROOT),
            }
        )
        for index, arm in enumerate(fixture["arm_registry"]):
            command = [
                str(ROOT / ".venv" / "bin" / "python"),
                "-B",
                SCRIPT_REL,
                "--worker",
                "--authorization",
                str(authorization_path.relative_to(ROOT)),
            ]
            invocation = {
                "arm_index": index,
                "arm_id": arm["arm_id"],
                "attempt": 1,
                "fresh_process_requested": True,
                "normalized_command": ".venv/bin/python -B experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_app_a2_run.py --worker --authorization experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i2/app-a2-activation-authorization.json",
            }
            try:
                completed = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=child_env,
                    input=json.dumps({"arm": arm}, sort_keys=True, separators=(",", ":")),
                    capture_output=True,
                    text=True,
                    timeout=float(execution["campaign_policy"]["maximum_wall_seconds_per_arm"]),
                )
                invocation.update(
                    {
                        "exit_code": completed.returncode,
                        "stderr_empty": completed.stderr == "",
                        "timed_out": False,
                        "fresh_process_started": True,
                    }
                )
                if completed.returncode != 0:
                    invocation["receipt_accepted"] = False
                    invocation["failure"] = "nonzero_exit"
                elif completed.stderr != "":
                    invocation["receipt_accepted"] = False
                    invocation["failure"] = "nonempty_stderr"
                else:
                    try:
                        child_receipt = json.loads(completed.stdout)
                        require(
                            child_receipt["arm_id"] == arm["arm_id"],
                            "child returned wrong arm",
                        )
                        receipts.append(child_receipt)
                        invocation["receipt_accepted"] = True
                    except Exception as exc:
                        invocation["receipt_accepted"] = False
                        invocation["failure"] = portable_failure_message(exc)
            except subprocess.TimeoutExpired:
                invocation.update(
                    {
                        "exit_code": None,
                        "stderr_empty": False,
                        "timed_out": True,
                        "fresh_process_started": True,
                        "receipt_accepted": False,
                        "failure": "arm_wall_time_exceeded",
                    }
                )
            except Exception as exc:
                invocation.update(
                    {
                        "exit_code": None,
                        "stderr_empty": False,
                        "timed_out": False,
                        "fresh_process_started": False,
                        "receipt_accepted": False,
                        "failure": portable_failure_message(exc),
                    }
                )
            child_invocations.append(invocation)

        analysis = analyze_receipts(receipts, fixture, execution)
        output: dict[str, Any] = {
            "artifact_id": "p2_i2_app_a2_runtime_evidence",
            "artifact_version": "1.0",
            "experiment_id": "2026-07-AE01",
            "generated_at": activation_freeze["frozen_at"],
            "iteration_id": "P2-I2-APP-A2",
            "status": "complete" if analysis["matrix_complete"] else "nonevaluable",
            "attempt_consumed": True,
            "authority": {
                "activation_authorization_path": str(authorization_path.relative_to(ROOT)),
                "activation_authorization_sha256": sha256_file(authorization_path),
                "activation_freeze_sha256": authorization["activation_freeze"]["sha256"],
                "activation_commit": git("rev-parse", "HEAD"),
                "graph_commit": activation_freeze["graph"]["commit"],
                "runner_sha256": sha256_file(Path(__file__)),
            },
            "campaign_receipt": {
                "campaign_invocations": 1,
                "campaign_retries": 0,
                "child_arm_starts": len(child_invocations),
                "child_arm_retries": 0,
                "fresh_process_per_arm": all(
                    row["fresh_process_started"] is True
                    for row in child_invocations
                ),
                "single_aggregate_output": True,
                "per_arm_persisted_files": 0,
                "child_invocations": child_invocations,
            },
            "arm_receipts": receipts,
            "analysis": analysis,
            "graph_after": {
                "commit": git("rev-parse", "HEAD", cwd=GRAPH_ROOT),
                "clean": git("status", "--short", cwd=GRAPH_ROOT) == "",
            },
            "claim_ceiling": execution["interpretation_contract"],
        }
        output["output_digest"] = digest_value(output)
        write_fd(fd, output)
        return 0 if analysis["matrix_complete"] else 1
    except Exception as exc:
        failed = {
            **claim,
            "status": "failed_closed",
            "app_a2_arm_starts": len(child_invocations),
            "completed_arm_receipts": receipts,
            "child_invocations": child_invocations,
            "failure": {
                "type": type(exc).__name__,
                "message": portable_failure_message(exc),
            },
            "scientific_result_assigned": False,
        }
        write_fd(fd, failed)
        return 1
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--campaign", action="store_true")
    mode.add_argument("--worker", action="store_true")
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    authorization_path = resolve_root_path(args.authorization).resolve()
    require(authorization_path.is_relative_to(ROOT), "authorization outside repository")
    if args.worker:
        require(args.output is None, "worker cannot accept output path")
        return worker_main(authorization_path)
    require(args.output is not None, "campaign output required")
    return campaign_main(authorization_path, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
