#!/usr/bin/env python3
"""Run quarantined APP-A1 native-interface conformance.

This harness uses sentinel values only. It cannot execute an APP-A2 arm,
evaluate the scientific gate signature, or assign an Appendix A result.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.metadata
import json
import math
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


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"
GRAPH_SOURCE_ROOT = GRAPH_ROOT / "src"
SCRIPT_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_app_a1_conform.py"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected object: {path}")
    return value


def deep_merge(base: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    """Return a recursive freeze revision without mutating retained base bytes."""

    merged = deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def resolve_freeze(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve an APP-A1 base freeze or one additive correction freeze."""

    raw = load_json(path)
    if "base_freeze" not in raw:
        return raw, {
            "freeze_kind": "base",
            "freeze_path": str(path.relative_to(ROOT)),
            "freeze_sha256": sha256_file(path),
        }
    base_ref = raw["base_freeze"]
    base_path = ROOT / str(base_ref["path"])
    require(base_path.is_file(), "base freeze missing")
    require(sha256_file(base_path) == base_ref["sha256"], "base freeze hash mismatch")
    merged = deep_merge(load_json(base_path), raw["overrides"])
    merged["correction"] = deepcopy(raw["correction"])
    return merged, {
        "freeze_kind": "additive_correction",
        "freeze_path": str(path.relative_to(ROOT)),
        "freeze_sha256": sha256_file(path),
        "base_freeze_path": str(base_path.relative_to(ROOT)),
        "base_freeze_sha256": sha256_file(base_path),
        "correction_freeze_artifact_id": raw["artifact_id"],
    }


def git(*args: str, cwd: Path = GRAPH_ROOT) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, condition: bool, observed: Any, expected: Any) -> None:
        row = {
            "check_id": check_id,
            "passed": bool(condition),
            "observed": observed,
            "expected": expected,
        }
        self.rows.append(row)
        require(condition, f"{check_id}: observed={observed!r} expected={expected!r}")


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def validate_freeze(
    freeze: Mapping[str, Any],
    freeze_path: Path,
    freeze_identity: Mapping[str, Any],
) -> dict[str, Any]:
    require(freeze["artifact_id"] == "P2-I2-APP-A1-FIXTURE-CONTROL-CONFORMANCE-FREEZE", "wrong freeze id")
    require(freeze["iteration_id"] == "P2-I2-APP-A1", "wrong iteration")
    require(freeze["status"] == "frozen_before_any_model_construction", "freeze not active")
    require(freeze["authority"]["candidate_free_conformance_authorized"] is True, "conformance closed")
    require(freeze["authority"]["app_a2_authorized"] is False, "APP-A2 unexpectedly open")
    require(freeze["authority"]["scientific_runtime_authorized"] is False, "scientific runtime open")
    run_policy = freeze["conformance"]["run_policy"]
    require(run_policy["evidence_invocations"] == 1, "wrong evidence count")
    require(run_policy["reconstruction_invocations"] == 1, "wrong reconstruction count")
    require(run_policy["retry_limit"] == 0, "retry must be zero")
    require(run_policy["scientific_values_allowed"] is False, "scientific values allowed")
    if freeze_identity["freeze_kind"] == "additive_correction":
        correction = freeze["correction"]
        require(correction["same_iteration"] is True, "correction left APP-A1")
        require(correction["original_attempt_consumed"] is True, "failed start not consumed")
        require(correction["replacement_attempt_authorized"] is True, "replacement closed")
        require(correction["original_retry_allowed"] is False, "original retry reopened")
        require(correction["intervention_semantics_changed"] is False, "clamp semantics changed")
        require(correction["app_a2_authorized"] is False, "APP-A2 opened by correction")
        for key in ("failed_start", "owner_authorization"):
            reference = correction[key]
            correction_path = ROOT / reference["path"]
            require(correction_path.is_file(), f"missing correction authority: {key}")
            require(
                sha256_file(correction_path) == reference["sha256"],
                f"correction authority hash mismatch: {key}",
            )
        intervention = freeze["conformance"]["carrier_clamp_intervention"]
        require(
            intervention["ledger_rebase_callable"]
            == "pygrc.models.build_lgrc9v3_packet_ledger",
            "wrong ledger rebase callable",
        )
        require(intervention["ledger_rebase_required_before_set_state"] is True, "ledger rebase optional")
        require(run_policy["original_failed_invocations"] == 1, "failed invocation missing")
        require(run_policy["original_invocation_consumed"] is True, "failed invocation not consumed")

    for row in freeze["authority"]["bound_rcae_files"]:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing RCAE file: {path}")
        require(sha256_file(path) == row["sha256"], f"RCAE hash mismatch: {path}")
    harness = freeze["authority"]["harness"]
    harness_path = ROOT / harness["path"]
    require(harness_path.resolve() == Path(__file__).resolve(), "wrong harness path")
    require(sha256_file(harness_path) == harness["sha256"], "harness hash mismatch")

    require(git("rev-parse", "HEAD") == freeze["authority"]["graph_commit"], "graph revision mismatch")
    require(git("status", "--short") == "", "graph tree dirty")
    for row in freeze["authority"]["bound_graph_files"]:
        path = GRAPH_ROOT / row["path"]
        require(path.is_file(), f"missing graph file: {path}")
        require(sha256_file(path) == row["sha256"], f"graph hash mismatch: {path}")

    expected_import = (GRAPH_SOURCE_ROOT / "pygrc" / "__init__.py").resolve()
    require(Path(pygrc.__file__).resolve() == expected_import, "wrong PyGRC import")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "RCAE venv inactive")
    require(any(Path(row).resolve() == GRAPH_SOURCE_ROOT.resolve() for row in sys.path if row), "checkout source binding absent")
    environment = freeze["environment"]
    require(platform.python_version() == environment["python_version"], "Python mismatch")
    versions = {
        package: importlib.metadata.version(package)
        for package in environment["direct_dependencies"]
    }
    require(versions == environment["direct_dependencies"], "dependency mismatch")

    scientific_numbers = {
        float(value)
        for operation in freeze["scientific_fixture"]["operation_vectors"].values()
        for value in operation.values()
    }
    sentinel_numbers = {
        float(value)
        for operation in freeze["conformance"]["sentinel_vectors"].values()
        for value in operation.values()
    }
    require(scientific_numbers.isdisjoint(sentinel_numbers), "sentinel overlaps scientific values")
    return {
        **dict(freeze_identity),
        "harness_path": SCRIPT_PATH,
        "harness_sha256": sha256_file(Path(__file__)),
        "graph_commit": freeze["authority"]["graph_commit"],
        "graph_clean": True,
        "pygrc_import_identity": {
            "repository_id": "graph-reflexive-coherence",
            "path": "src/pygrc/__init__.py",
        },
        "python_version": platform.python_version(),
        "invoked_executable": ".venv/bin/python",
        "venv_prefix": ".venv",
        "dependency_versions": versions,
    }


def build_model(
    freeze: Mapping[str, Any],
    *,
    label_overrides: Mapping[str, str] | None = None,
) -> tuple[LGRC9V3, dict[str, int], dict[str, int]]:
    topology = freeze["topology"]
    graph = PortGraphBackend()
    role_ids: dict[str, int] = {}
    for node in topology["nodes"]:
        role = str(node["role"])
        label = role if label_overrides is None else label_overrides.get(role, role)
        node_id = graph.add_node({"label": label})
        require(node_id == int(node["node_id"]), f"node id mismatch: {role}")
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
        require(edge_id == int(edge["edge_id"]), f"edge id mismatch: {edge['edge_role']}")
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

    initial = freeze["conformance"]["initial_coherence"]
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


def drain_pair(model: LGRC9V3) -> list[dict[str, Any]]:
    results = [model.step(), model.step()]
    return [
        {
            "processed_event_kind": result.bookkeeping["processed_event_kind"],
            "processed_event_id": result.bookkeeping["processed_event_id"],
            "budget_error": next(
                (
                    float(event.payload["budget_error"])
                    for event in result.events
                    if "budget_error" in event.payload
                ),
                0.0,
            ),
        }
        for result in results
    ]


def transfer(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    *,
    source: str,
    target: str,
    amount: float,
    pair_index: int,
    packet_index: int,
) -> dict[str, Any]:
    edge_role = "__".join(sorted((source, target)))
    departure = float(2 * pair_index + 1)
    arrival = float(2 * pair_index + 2)
    before = coherences(model, role_ids)
    model.schedule_packet_departure(
        source_node_id=role_ids[source],
        target_node_id=role_ids[target],
        edge_id=edge_ids[edge_role],
        amount=float(amount),
        departure_event_time_key=departure,
        arrival_event_time_key=arrival,
        scheduler_event_index=int(2 * pair_index + 1),
        packet_index=packet_index,
        source_lineage_id=f"app-a1:{source}",
        target_lineage_id=f"app-a1:{target}",
    )
    events = drain_pair(model)
    after = coherences(model, role_ids)
    return {
        "source": source,
        "target": target,
        "edge_role": edge_role,
        "amount": float(amount),
        "departure_event_time_key": departure,
        "arrival_event_time_key": arrival,
        "source_delta": after[source] - before[source],
        "target_delta": after[target] - before[target],
        "events": events,
    }


def apply_operations(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
    *,
    common: bool,
) -> list[dict[str, Any]]:
    vectors = freeze["conformance"]["sentinel_vectors"]
    axes = freeze["measurement_authority"]["carrier_axes"]
    prefix = "c" if common else "d"
    receipts: list[dict[str, Any]] = []
    pair = 0
    packet = 0
    for axis in axes:
        receipts.append(
            transfer(
                model,
                role_ids,
                edge_ids,
                source="s_g",
                target=f"{prefix}_{axis}",
                amount=float(vectors["G"][axis]),
                pair_index=pair,
                packet_index=packet,
            )
        )
        pair += 1
        packet += 1
    for axis in axes:
        receipts.append(
            transfer(
                model,
                role_ids,
                edge_ids,
                source=f"{prefix}_{axis}",
                target="s_e",
                amount=float(vectors["E"][axis]),
                pair_index=pair,
                packet_index=packet,
            )
        )
        pair += 1
        packet += 1
    receipts.append(
        transfer(
            model,
            role_ids,
            edge_ids,
            source=f"{prefix}_boundary",
            target="s_p",
            amount=float(vectors["P"]["boundary_out"]),
            pair_index=pair,
            packet_index=packet,
        )
    )
    pair += 1
    packet += 1
    for axis in ("environment", "support", "distinguishability"):
        receipts.append(
            transfer(
                model,
                role_ids,
                edge_ids,
                source="s_p",
                target=f"{prefix}_{axis}",
                amount=float(vectors["P"][axis]),
                pair_index=pair,
                packet_index=packet,
            )
        )
        pair += 1
        packet += 1
    return receipts


def produce_response(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    axes = freeze["measurement_authority"]["carrier_axes"]
    fraction = float(freeze["measurement_authority"]["retention_fraction"])
    pre = coherences(model, role_ids)
    routes = {
        role_ids[f"c_{axis}"]: [
            {
                "target_node_id": role_ids["r"],
                "edge_id": edge_ids["__".join(sorted((f"c_{axis}", "r")))],
                "amount_fraction": fraction,
            }
        ]
        for axis in axes
    }
    model.set_causal_flux_routes(routes)
    production = model.produce_events(
        policy=LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FLUX_ROUTE
    )
    records = list(production.production_records)
    require(len(records) == len(axes), "response route count mismatch")
    require(all(row.reason_code == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_PACKET_DEPARTURE_SCHEDULED for row in records), "response not scheduled")
    steps = model.run_event_queue(max_events=2 * len(axes))
    require(len(steps) == 2 * len(axes), "response event count mismatch")
    require(not model.get_state().packet_ledger.event_queue_records, "response queue not empty")
    post = coherences(model, role_ids)
    response_by_axis = {
        axis: pre[f"c_{axis}"] * fraction
        for axis in axes
    }
    return {
        "producer_policy": production.producer_policy,
        "production_record_count": len(records),
        "reason_codes": [row.reason_code for row in records],
        "pre_r_carrier": {axis: pre[f"c_{axis}"] for axis in axes},
        "response_by_axis": response_by_axis,
        "r_delta": post["r"] - pre["r"],
        "response_event_count": len(steps),
        "post_r_carrier": {axis: post[f"c_{axis}"] for axis in axes},
        "source_node_ids": sorted(int(row.trigger_node_id) for row in records),
    }


def rebase_packet_ledger_after_intervention(state: Any) -> dict[str, Any]:
    """Rebase PyGRC's conserved-total projection after an imposed state edit.

    The clamp is an explicit control intervention, not packet transport.  The
    public builder preserves packet/event history and policies while making the
    ledger describe the newly imposed node coherences before later native work.
    """

    old = state.packet_ledger
    require(old is not None, "packet ledger absent before intervention")
    require(not old.event_queue_records, "intervention requires an empty event queue")
    old_node_total = float(old.node_coherence_total)
    old_conserved_total = float(old.conserved_budget_total)
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
        packet_transport_through_topology_change=(
            old.packet_transport_through_topology_change
        ),
        identity_acceptance_allowed=old.identity_acceptance_allowed,
        collapse_allowed=old.collapse_allowed,
    )
    rebased = state.packet_ledger
    return {
        "mechanism": "pygrc.models.build_lgrc9v3_packet_ledger",
        "packet_history_preserved": rebased.packet_records == old.packet_records,
        "packet_event_history_preserved": (
            rebased.packet_event_records == old.packet_event_records
        ),
        "queue_was_empty": not old.event_queue_records,
        "old_node_coherence_total": old_node_total,
        "new_node_coherence_total": float(rebased.node_coherence_total),
        "old_conserved_budget_total": old_conserved_total,
        "new_conserved_budget_total": float(rebased.conserved_budget_total),
        "new_budget_error": float(rebased.budget_error),
    }


def branch(
    freeze: Mapping[str, Any],
    *,
    common: bool,
    label_overrides: Mapping[str, str] | None = None,
    clamp: bool = False,
) -> tuple[LGRC9V3, dict[str, int], dict[str, Any]]:
    model, role_ids, edge_ids = build_model(freeze, label_overrides=label_overrides)
    baseline_identity = digest_lgrc9v3_restoration_identity_v2(model)
    before = coherences(model, role_ids)
    receipts = apply_operations(model, role_ids, edge_ids, freeze, common=common)
    pre_r = coherences(model, role_ids)
    intervention = None
    if clamp:
        state = deepcopy(model.get_state())
        for axis in freeze["measurement_authority"]["carrier_axes"]:
            state.base_state.nodes[role_ids[f"c_{axis}"]].coherence = before[f"c_{axis}"]
        ledger_rebase = rebase_packet_ledger_after_intervention(state)
        identity_before = digest_lgrc9v3_restoration_identity_v2(model)
        model.set_state(state)
        identity_after = digest_lgrc9v3_restoration_identity_v2(model)
        intervention = {
            "kind": "carrier_clamp_to_registered_baseline",
            "identity_before": identity_before,
            "identity_after": identity_after,
            "identity_changed": identity_before != identity_after,
            "packet_ledger_rebase": ledger_rebase,
        }
        pre_r = coherences(model, role_ids)
    response = produce_response(model, role_ids, edge_ids, freeze)
    return model, role_ids, {
        "baseline_identity": baseline_identity,
        "operation_receipts": receipts,
        "pre_r_coherence": pre_r,
        "intervention": intervention,
        "response": response,
        "final_identity": digest_lgrc9v3_restoration_identity_v2(model),
    }


def zero_net_round_trip(freeze: Mapping[str, Any]) -> dict[str, Any]:
    model, role_ids, edge_ids = build_model(freeze)
    amount = float(freeze["conformance"]["zero_net_round_trip_amount"])
    before = coherences(model, role_ids)
    identity_before = digest_lgrc9v3_restoration_identity_v2(model)
    first = transfer(
        model,
        role_ids,
        edge_ids,
        source="c_boundary",
        target="s_p",
        amount=amount,
        pair_index=0,
        packet_index=0,
    )
    second = transfer(
        model,
        role_ids,
        edge_ids,
        source="s_p",
        target="c_boundary",
        amount=amount,
        pair_index=1,
        packet_index=1,
    )
    after = coherences(model, role_ids)
    return {
        "carrier_delta": after["c_boundary"] - before["c_boundary"],
        "participant_delta": after["s_p"] - before["s_p"],
        "packet_receipt_count": 2,
        "receipts": [first, second],
        "state_numeric_returned": after["c_boundary"] == before["c_boundary"] and after["s_p"] == before["s_p"],
        "history_identity_changed": digest_lgrc9v3_restoration_identity_v2(model) != identity_before,
    }


def restoration_receipt(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    baseline_identity: str,
) -> dict[str, Any]:
    before_save = digest_lgrc9v3_restoration_identity_v2(model)
    with tempfile.TemporaryDirectory(prefix="p2-i2-app-a1-") as directory:
        path = Path(directory) / "snapshot.json"
        model.save(str(path))
        loaded = LGRC9V3.load(str(path))
    after_load = digest_lgrc9v3_restoration_identity_v2(loaded)
    model.step()
    loaded.step()
    after_empty_step_original = digest_lgrc9v3_restoration_identity_v2(model)
    after_empty_step_loaded = digest_lgrc9v3_restoration_identity_v2(loaded)
    model.reset()
    loaded.reset()
    after_reset_original = digest_lgrc9v3_restoration_identity_v2(model)
    after_reset_loaded = digest_lgrc9v3_restoration_identity_v2(loaded)
    return {
        "identity_before_save": before_save,
        "identity_after_load": after_load,
        "save_load_identity_equal": before_save == after_load,
        "empty_step_identity_equal": after_empty_step_original == after_empty_step_loaded,
        "original_reset_to_baseline": after_reset_original == baseline_identity,
        "loaded_reset_to_baseline": after_reset_loaded == baseline_identity,
        "post_reset_coherence": coherences(loaded, role_ids),
    }


def build_output(
    freeze: Mapping[str, Any],
    freeze_path: Path,
    freeze_identity: Mapping[str, Any],
) -> dict[str, Any]:
    provenance = validate_freeze(freeze, freeze_path, freeze_identity)
    checks = Checks()
    tolerance = float(freeze["measurement_authority"]["runtime_tolerance"])
    axes = freeze["measurement_authority"]["carrier_axes"]
    initial = freeze["conformance"]["initial_coherence"]
    vectors = freeze["conformance"]["sentinel_vectors"]

    common_model, common_roles, common = branch(freeze, common=True)
    diverted_model, diverted_roles, diverted = branch(freeze, common=False)
    permuted_model, permuted_roles, permuted = branch(
        freeze,
        common=True,
        label_overrides=freeze["conformance"]["label_permutation"],
    )
    clamped_model, clamped_roles, clamped = branch(freeze, common=True, clamp=True)

    expected_delta = {
        "environment": float(vectors["G"]["environment"]) - float(vectors["E"]["environment"]) + float(vectors["P"]["environment"]),
        "support": float(vectors["G"]["support"]) - float(vectors["E"]["support"]) + float(vectors["P"]["support"]),
        "distinguishability": float(vectors["G"]["distinguishability"]) - float(vectors["E"]["distinguishability"]) + float(vectors["P"]["distinguishability"]),
        "boundary": float(vectors["G"]["boundary"]) - float(vectors["E"]["boundary"]) - float(vectors["P"]["boundary_out"]),
    }
    for axis in axes:
        observed = common["response"]["pre_r_carrier"][axis]
        expected = float(initial[f"c_{axis}"]) + expected_delta[axis]
        checks.add(f"common.pre_r.{axis}", close(observed, expected, tolerance), observed, expected)
        diverted_observed = diverted["response"]["pre_r_carrier"][axis]
        diverted_expected = float(initial[f"c_{axis}"])
        checks.add(f"diverted.pre_r.{axis}", close(diverted_observed, diverted_expected, tolerance), diverted_observed, diverted_expected)
        checks.add(
            f"label_permutation.response.{axis}",
            close(permuted["response"]["response_by_axis"][axis], common["response"]["response_by_axis"][axis], tolerance),
            permuted["response"]["response_by_axis"][axis],
            common["response"]["response_by_axis"][axis],
        )
        checks.add(
            f"clamp.response.{axis}",
            close(clamped["response"]["pre_r_carrier"][axis], float(initial[f"c_{axis}"]), tolerance),
            clamped["response"]["pre_r_carrier"][axis],
            float(initial[f"c_{axis}"]),
        )

    checks.add("common.operation_receipts", len(common["operation_receipts"]) == 12, len(common["operation_receipts"]), 12)
    checks.add("diverted.operation_receipts", len(diverted["operation_receipts"]) == 12, len(diverted["operation_receipts"]), 12)
    checks.add("common.response_receipts", common["response"]["production_record_count"] == 4, common["response"]["production_record_count"], 4)
    checks.add("diverted.response_receipts", diverted["response"]["production_record_count"] == 4, diverted["response"]["production_record_count"], 4)
    checks.add("r_sources_carrier_only", common["response"]["source_node_ids"] == sorted(common_roles[f"c_{axis}"] for axis in axes), common["response"]["source_node_ids"], sorted(common_roles[f"c_{axis}"] for axis in axes))
    checks.add("carrier_clamp_identity_changed", clamped["intervention"]["identity_changed"] is True, clamped["intervention"]["identity_changed"], True)

    zero = zero_net_round_trip(freeze)
    checks.add("valid_zero_numeric_return", zero["state_numeric_returned"] is True, zero["state_numeric_returned"], True)
    checks.add("valid_zero_receipts", zero["packet_receipt_count"] == 2, zero["packet_receipt_count"], 2)
    checks.add("valid_zero_history_retained", zero["history_identity_changed"] is True, zero["history_identity_changed"], True)

    restoration = restoration_receipt(common_model, common_roles, common["baseline_identity"])
    checks.add("save_load_identity", restoration["save_load_identity_equal"] is True, restoration["save_load_identity_equal"], True)
    checks.add("empty_step_continuation", restoration["empty_step_identity_equal"] is True, restoration["empty_step_identity_equal"], True)
    checks.add("original_reset", restoration["original_reset_to_baseline"] is True, restoration["original_reset_to_baseline"], True)
    checks.add("loaded_reset", restoration["loaded_reset_to_baseline"] is True, restoration["loaded_reset_to_baseline"], True)

    require(git("status", "--short") == "", "graph changed during conformance")
    output: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a1_runtime_conformance",
        "artifact_version": "1.0",
        "experiment_id": "2026-07-AE01",
        "generated_at": freeze["frozen_at"],
        "iteration_id": "P2-I2-APP-A1",
        "status": "passed" if all(row["passed"] for row in checks.rows) else "failed",
        "evidence_class": "candidate_free_native_interface_conformance_only",
        "provenance": provenance,
        "branches": {
            "native_common": common,
            "all_diverted": diverted,
            "label_permuted": permuted,
            "carrier_clamped": clamped,
            "valid_zero_round_trip": zero,
        },
        "restoration": restoration,
        "checks": checks.rows,
        "checks_passed": sum(1 for row in checks.rows if row["passed"]),
        "checks_total": len(checks.rows),
        "graph_after": {
            "commit": git("rev-parse", "HEAD"),
            "clean": git("status", "--short") == "",
        },
        "quarantine": {
            "scientific_vectors_used": False,
            "app_a2_arms_executed": 0,
            "scientific_gate_signatures_evaluated": 0,
            "support_or_falsification_assigned": False,
            "app_a1_accepted": False,
            "commit_authorized": False,
        },
    }
    output["output_digest"] = digest_value(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    freeze_path = (ROOT / args.freeze).resolve()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    freeze, freeze_identity = resolve_freeze(freeze_path)
    output = build_output(freeze, freeze_path, freeze_identity)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(canonical_bytes(output))
    print(json.dumps({
        "status": output["status"],
        "checks_passed": output["checks_passed"],
        "checks_total": output["checks_total"],
        "output_digest": output["output_digest"],
    }, sort_keys=True))
    return 0 if output["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
