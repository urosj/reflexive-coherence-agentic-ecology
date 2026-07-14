#!/usr/bin/env python3
"""Frozen P2-I2-I03AR1 state-carried implementation conformance harness.

This is quarantined implementation evidence. It must not be used for I04/I05
calibration, I06 registration, I08 execution, or an AE01-H-L02 conclusion.
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
    LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY,
    LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED,
    LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SUBTHRESHOLD,
    LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS,
    PortEdge,
    digest_lgrc9v3_restoration_identity_v2,
)


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = Path("/home/uros/Documents/RC-github/graph-reflexive-coherence")
GRAPH_SOURCE_ROOT = GRAPH_ROOT / "src"
SCRIPT_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03ar1_conform.py"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _git(*args: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(GRAPH_ROOT), *args),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _graph_guard() -> dict[str, Any]:
    return {
        "revision": _git("rev-parse", "HEAD"),
        "status_porcelain": _git("status", "--porcelain=v1", "--untracked-files=all"),
    }


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _merge_mapping(base: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(dict(base))
    for key, value in overrides.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = _merge_mapping(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _resolve_freeze(path: Path) -> dict[str, Any]:
    candidate = _load_json(path)
    base_reference = candidate.get("base_freeze")
    if not isinstance(base_reference, Mapping):
        return candidate
    base_path = ROOT / str(base_reference["path"])
    _require(base_path.is_file(), f"missing base freeze: {base_path}")
    _require(_sha256(base_path) == base_reference["sha256"], "base freeze digest mismatch")
    overrides = candidate.get("overrides")
    _require(isinstance(overrides, Mapping), "freeze revision overrides must be a mapping")
    resolved = _merge_mapping(_load_json(base_path), overrides)
    resolved["freeze_revision"] = {
        "artifact_id": candidate["artifact_id"],
        "artifact_version": candidate["artifact_version"],
        "correction_iteration_id": candidate["correction_iteration_id"],
        "path": str(path.relative_to(ROOT)),
        "sha256": _sha256(path),
        "base_path": str(base_path.relative_to(ROOT)),
        "base_sha256": _sha256(base_path),
    }
    return resolved


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _derived_response_delta_matches(
    observed: float,
    expected: float,
    freeze: Mapping[str, Any],
) -> bool:
    comparator = freeze["assertions"]["derived_response_delta_comparator"]
    return math.isclose(
        observed,
        expected,
        rel_tol=float(comparator["relative_tolerance"]),
        abs_tol=float(comparator["absolute_tolerance"]),
    )


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
        _require(condition, f"{check_id} failed: observed={observed!r} expected={expected!r}")


def _validate_freeze(freeze: Mapping[str, Any], freeze_path: Path) -> dict[str, Any]:
    _require(freeze.get("artifact_id") == "P2-I2-I03AR1-STATE-CARRIED-RUNTIME-CONFORMANCE-INPUT-FREEZE", "wrong freeze artifact_id")
    _require(freeze.get("iteration_id") == "P2-I2-I03AR1", "wrong iteration_id")
    _require(freeze.get("pool_dependence_mode") == "state_carried", "wrong dependence mode")
    _require(freeze.get("runtime_authorized") is True, "runtime is not authorized by freeze")
    run_policy = freeze["run_policy"]
    _require(run_policy["evidence_invocations"] == 1, "evidence invocation count must be one")
    _require(run_policy["reconstruction_invocations"] == 1, "reconstruction invocation count must be one")
    _require(run_policy["retry_limit"] == 0, "retry limit must be zero")
    _require(run_policy["parameter_search_allowed"] is False, "parameter search must be prohibited")
    _require(run_policy["rescue_variants_allowed"] is False, "rescue variants must be prohibited")

    authority = freeze["authority"]
    bound = authority["bound_rcae_artifacts"]
    for item in bound:
        path = ROOT / item["path"]
        _require(path.is_file(), f"missing bound RCAE artifact: {path}")
        _require(_sha256(path) == item["sha256"], f"RCAE artifact digest mismatch: {path}")

    harness = authority["harness"]
    harness_path = ROOT / harness["path"]
    _require(harness_path.resolve() == Path(__file__).resolve(), "unexpected harness path")
    _require(_sha256(harness_path) == harness["sha256"], "harness digest mismatch")

    graph_before = _graph_guard()
    _require(graph_before["revision"] == authority["graph_revision"], "graph revision mismatch")
    _require(graph_before["status_porcelain"] == "", "graph checkout is not clean")
    source_digests: dict[str, str] = {}
    for item in authority["bound_graph_sources"]:
        path = GRAPH_ROOT / item["path"]
        _require(path.is_file(), f"missing graph source: {path}")
        actual = _sha256(path)
        _require(actual == item["sha256"], f"graph source digest mismatch: {path}")
        source_digests[item["path"]] = actual

    expected_import = (GRAPH_SOURCE_ROOT / "pygrc" / "__init__.py").resolve()
    actual_import = Path(pygrc.__file__).resolve()
    _require(actual_import == expected_import, "PyGRC import is not from admitted checkout")
    environment = freeze["environment"]
    _require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "RCAE .venv is not active")
    dependency_versions = {
        name: importlib.metadata.version(name)
        for name in environment["direct_dependencies"]
    }
    _require(dependency_versions == environment["direct_dependencies"], "direct dependency version mismatch")
    _require(platform.python_version() == environment["python_version"], "Python version mismatch")
    _require(Path(sys.path[0]).resolve() != GRAPH_SOURCE_ROOT.resolve(), "script directory unexpectedly aliases graph source root")
    _require(any(Path(item).resolve() == GRAPH_SOURCE_ROOT.resolve() for item in sys.path if item), "admitted graph source root absent from sys.path")

    return {
        "freeze_path": str(freeze_path.relative_to(ROOT)),
        "freeze_sha256": _sha256(freeze_path),
        "harness_path": SCRIPT_RELATIVE_PATH,
        "harness_sha256": _sha256(Path(__file__)),
        "graph_before": graph_before,
        "graph_source_digests": source_digests,
        "pygrc_import_file": str(actual_import),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "sys_executable": sys.executable,
        "sys_prefix": sys.prefix,
        "direct_dependency_versions": dependency_versions,
    }


def _build_model(freeze: Mapping[str, Any]) -> tuple[LGRC9V3, dict[str, int], dict[str, int]]:
    fixture = freeze["fixture"]
    graph = PortGraphBackend()
    role_ids: dict[str, int] = {}
    for node in fixture["nodes"]:
        node_id = graph.add_node({"label": node["role"]})
        _require(node_id == node["node_id"], f"node id mismatch for {node['role']}")
        role_ids[node["role"]] = node_id

    next_slot = {node_id: 0 for node_id in role_ids.values()}
    edge_ids: dict[str, int] = {}
    port_edges: dict[int, PortEdge] = {}
    for edge in fixture["edges"]:
        source = role_ids[edge["source"]]
        target = role_ids[edge["target"]]
        source_slot = next_slot[source]
        target_slot = next_slot[target]
        edge_id = graph.connect_ports(
            source,
            source_slot,
            target,
            target_slot,
            {"kind": edge["edge_role"]},
        )
        _require(edge_id == edge["edge_id"], f"edge id mismatch for {edge['edge_role']}")
        next_slot[source] += 1
        next_slot[target] += 1
        edge_ids[edge["edge_role"]] = edge_id
        port_edges[edge_id] = PortEdge(
            source,
            source_slot + 1,
            target,
            target_slot + 1,
            conductance=1.0,
            flux_uv=0.0,
        )

    node_states = {
        role_ids[node["role"]]: GRC9V3NodeState(coherence=float(node["initial_coherence"]))
        for node in fixture["nodes"]
    }
    unit_edges = {edge_id: 1.0 for edge_id in edge_ids.values()}
    zero_edges = {edge_id: 0.0 for edge_id in edge_ids.values()}
    state = GRC9V3State(
        topology=graph,
        nodes=node_states,
        port_edges=port_edges,
        base_conductance=unit_edges,
        geometric_length=unit_edges,
        temporal_delay=unit_edges,
        flux_coupling=zero_edges,
    )
    modes = fixture["causal_modes"]
    params = {
        "dt": fixture["dt"],
        "causal_modes": {
            "causal_layer_mode": CAUSAL_LAYER_MODE_PACKETIZED_FIXED_TOPOLOGY,
            "lgrc_runtime_level": LGRC_RUNTIME_LEVEL_LGRC2,
            "lapse_policy": LAPSE_POLICY_UNIT,
            "edge_delay_policy": EDGE_DELAY_POLICY_CONSTANT_DELAY,
            "event_time_policy": modes["event_time_policy"],
            "proper_time_accumulation_policy": modes["proper_time_accumulation_policy"],
            "causal_pulse_substrate_surface_enabled": True,
            "causal_pulse_substrate_surface_policy": LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS,
            "causal_pulse_substrate_surface_validated": False,
        },
    }
    return LGRC9V3.from_state(state, params), role_ids, edge_ids


def _queue_signature(model: LGRC9V3) -> list[list[Any]]:
    return [
        [
            event.event_time_key,
            event.scheduler_event_index,
            event.event_kind,
            event.event_id,
            event.packet_id,
        ]
        for event in model.get_state().packet_ledger.event_queue_records
    ]


def _coherences(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, float]:
    nodes = model.get_state().base_state.nodes
    return {role: float(nodes[node_id].coherence) for role, node_id in sorted(role_ids.items())}


def _packet_records(model: LGRC9V3) -> list[dict[str, Any]]:
    return [row.to_record() for row in model.get_state().packet_ledger.packet_records]


def _drain(model: LGRC9V3, event_count: int) -> None:
    for _ in range(event_count):
        _require(bool(model.get_state().packet_ledger.event_queue_records), "queue drained before frozen event count")
        model.step()
    _require(not model.get_state().packet_ledger.event_queue_records, "queue not drained at frozen event count")


def _schedule_contributions(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
    specs: Sequence[Mapping[str, Any]],
) -> None:
    for spec in specs:
        model.schedule_packet_departure(
            source_node_id=role_ids[spec["source"]],
            target_node_id=role_ids[spec["target"]],
            edge_id=edge_ids[spec["edge_role"]],
            amount=float(spec["amount"]),
            departure_event_time_key=float(spec["departure_event_time_key"]),
            arrival_event_time_key=float(spec["arrival_event_time_key"]),
            scheduler_event_index=int(spec["scheduler_event_index"]),
            packet_index=int(spec["packet_index"]),
            source_lineage_id=str(spec["source_lineage_id"]),
            target_lineage_id=str(spec["target_lineage_id"]),
        )
    _drain(model, 2 * len(specs))


def _neutral_contact(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
) -> None:
    spec = freeze["fixture"]["neutral_contact"]
    model.schedule_packet_departure(
        source_node_id=role_ids[spec["source"]],
        target_node_id=role_ids[spec["target"]],
        edge_id=edge_ids[spec["edge_role"]],
        amount=float(spec["amount"]),
        departure_event_time_key=float(spec["departure_event_time_key"]),
        arrival_event_time_key=float(spec["arrival_event_time_key"]),
        scheduler_event_index=int(spec["scheduler_event_index"]),
        packet_index=int(spec["packet_index"]),
        source_lineage_id=str(spec["source_lineage_id"]),
        target_lineage_id=str(spec["target_lineage_id"]),
    )
    _drain(model, 2)


def _prepare_feedback(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
    *,
    front_role: str = "P",
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
) -> dict[str, Any]:
    response = freeze["fixture"]["response"]
    row = model.emit_feedback_eligibility_surface_row(
        front_node_ids=(role_ids[front_role],),
        rear_node_ids=(role_ids["B_ref"],),
        reference_delta=float(response["reference_delta"]),
        feedback_threshold=float(response["threshold"]),
    )
    model.set_feedback_coupled_pulse_producer(
        source_node_id=role_ids[response_source],
        target_node_id=role_ids[response_target],
        edge_id=edge_ids[response_edge],
        threshold=float(response["threshold"]),
        packet_amount=float(response["packet_amount"]),
        expected_polarity=str(response["expected_polarity"]),
        expected_source_surface_digest=None,
        arrival_event_time_key=float(response["arrival_event_time_key"]),
    )
    return {
        "surface_digest": row.surface_digest,
        "front_node_ids": list(row.surface_update_policy["declared_front_node_ids"]),
        "rear_node_ids": list(row.surface_update_policy["declared_rear_node_ids"]),
        "front_mass": float(row.surface_values_after["front_mass"]),
        "rear_mass": float(row.surface_values_after["rear_mass"]),
        "boundary_polarity_score": float(row.surface_values_after["boundary_polarity_score"]),
        "feedback_threshold": float(row.surface_values_after["feedback_threshold"]),
        "expected_source_surface_digest": None,
    }


def _execute_feedback(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    *,
    response_target: str = "B",
) -> dict[str, Any]:
    before = float(model.get_state().base_state.nodes[role_ids[response_target]].coherence)
    result = model.produce_events(
        policy=LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY
    )
    _require(len(result.production_records) == 1, "expected exactly one producer record")
    record = result.production_records[0]
    scheduled = record.reason_code == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED
    if scheduled:
        _drain(model, 2)
    else:
        _require(not model.get_state().packet_ledger.event_queue_records, "negative feedback enqueued work")
    after = float(model.get_state().base_state.nodes[role_ids[response_target]].coherence)
    return {
        "reason_code": record.reason_code,
        "scheduled": scheduled,
        "producer_state_mutated": bool(result.state_mutated),
        "scheduled_event_kind": record.scheduled_event_kind,
        "response_target": response_target,
        "target_coherence_before": before,
        "target_coherence_after": after,
        "producer_mutated_coherence": bool(record.observed_evidence.get("producer_mutated_coherence", False)),
        "direct_claim_write": bool(record.observed_evidence.get("direct_claim_write", False)),
        "threshold_source": record.observed_evidence.get("threshold_source"),
        "polarity_policy_source": record.observed_evidence.get("polarity_policy_source"),
    }


def _run_standard_branch(
    branch_id: str,
    freeze: Mapping[str, Any],
    contribution_key: str | None,
    checks: Checks,
    *,
    front_role: str = "P",
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
) -> dict[str, Any]:
    model, role_ids, edge_ids = _build_model(freeze)
    if contribution_key is not None:
        _schedule_contributions(
            model,
            role_ids,
            edge_ids,
            freeze,
            freeze["fixture"]["contribution_sequences"][contribution_key],
        )
    _neutral_contact(model, role_ids, edge_ids, freeze)
    feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        freeze,
        front_role=front_role,
        response_source=response_source,
        response_target=response_target,
        response_edge=response_edge,
    )
    response = _execute_feedback(model, role_ids, response_target=response_target)
    expected = freeze["assertions"]["branches"][branch_id]
    coherences = _coherences(model, role_ids)
    checks.add(f"{branch_id}.score", feedback["boundary_polarity_score"] == expected["score"], feedback["boundary_polarity_score"], expected["score"])
    checks.add(f"{branch_id}.reason", response["reason_code"] == expected["reason_code"], response["reason_code"], expected["reason_code"])
    checks.add(f"{branch_id}.scheduled", response["scheduled"] is expected["scheduled"], response["scheduled"], expected["scheduled"])
    for role, value in expected["coherences"].items():
        checks.add(f"{branch_id}.coherence.{role}", coherences[role] == value, coherences[role], value)
    response_delta = response["target_coherence_after"] - response["target_coherence_before"]
    checks.add(
        f"{branch_id}.response_delta",
        _derived_response_delta_matches(
            response_delta,
            expected["response_delta"],
            freeze,
        ),
        response_delta,
        expected["response_delta"],
    )
    checks.add(f"{branch_id}.front_mask", feedback["front_node_ids"] == [role_ids[front_role]], feedback["front_node_ids"], [role_ids[front_role]])
    checks.add(f"{branch_id}.rear_mask", feedback["rear_node_ids"] == [role_ids["B_ref"]], feedback["rear_node_ids"], [role_ids["B_ref"]])
    checks.add(f"{branch_id}.queue_drained", _queue_signature(model) == [], _queue_signature(model), [])
    if response["scheduled"]:
        checks.add(f"{branch_id}.producer_no_direct_coherence", response["producer_mutated_coherence"] is False, response["producer_mutated_coherence"], False)
        checks.add(f"{branch_id}.producer_no_claim_write", response["direct_claim_write"] is False, response["direct_claim_write"], False)
    return {
        "branch_id": branch_id,
        "coherences": coherences,
        "feedback": feedback,
        "response": response,
        "packet_records": _packet_records(model),
        "queue_signature_after": _queue_signature(model),
        "restoration_identity_v2_after": digest_lgrc9v3_restoration_identity_v2(model),
    }


def _run_carrier_debit(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    branch_id = "carrier_debit"
    model, role_ids, edge_ids = _build_model(freeze)
    _schedule_contributions(model, role_ids, edge_ids, freeze, freeze["fixture"]["contribution_sequences"]["combined_s1_s2"])
    spec = freeze["fixture"]["carrier_debit"]
    model.schedule_packet_departure(
        source_node_id=role_ids[spec["source"]],
        target_node_id=role_ids[spec["target"]],
        edge_id=edge_ids[spec["edge_role"]],
        amount=float(spec["amount"]),
        departure_event_time_key=float(spec["departure_event_time_key"]),
        arrival_event_time_key=float(spec["arrival_event_time_key"]),
        scheduler_event_index=int(spec["scheduler_event_index"]),
        packet_index=int(spec["packet_index"]),
        source_lineage_id=str(spec["source_lineage_id"]),
        target_lineage_id=str(spec["target_lineage_id"]),
    )
    _drain(model, 2)
    _neutral_contact(model, role_ids, edge_ids, freeze)
    feedback = _prepare_feedback(model, role_ids, edge_ids, freeze)
    response = _execute_feedback(model, role_ids)
    expected = freeze["assertions"]["branches"][branch_id]
    coherences = _coherences(model, role_ids)
    for role, value in expected["coherences"].items():
        checks.add(f"carrier_debit.coherence.{role}", coherences[role] == value, coherences[role], value)
    checks.add("carrier_debit.score", feedback["boundary_polarity_score"] == expected["score"], feedback["boundary_polarity_score"], expected["score"])
    checks.add("carrier_debit.reason", response["reason_code"] == expected["reason_code"], response["reason_code"], expected["reason_code"])
    response_delta = response["target_coherence_after"] - response["target_coherence_before"]
    checks.add(
        "carrier_debit.response_delta",
        _derived_response_delta_matches(
            response_delta,
            expected["response_delta"],
            freeze,
        ),
        response_delta,
        expected["response_delta"],
    )
    return {
        "branch_id": branch_id,
        "coherences": coherences,
        "feedback": feedback,
        "response": response,
        "packet_records": _packet_records(model),
        "queue_signature_after": _queue_signature(model),
        "restoration_identity_v2_after": digest_lgrc9v3_restoration_identity_v2(model),
    }


def _run_private_partition(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    branch_id = "private_partition"
    model, role_ids, edge_ids = _build_model(freeze)
    _schedule_contributions(model, role_ids, edge_ids, freeze, freeze["fixture"]["contribution_sequences"]["private_partition"])
    _neutral_contact(model, role_ids, edge_ids, freeze)
    first_feedback = _prepare_feedback(model, role_ids, edge_ids, freeze, front_role="P1_private")
    first_response = _execute_feedback(model, role_ids)
    second_feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        freeze,
        front_role="P2_private",
        response_source="A_alt",
        response_target="B_alt",
        response_edge="A_alt_to_B_alt",
    )
    second_response = _execute_feedback(model, role_ids, response_target="B_alt")
    expected = freeze["assertions"]["branches"][branch_id]
    masks = [first_feedback["front_node_ids"], second_feedback["front_node_ids"]]
    scores = [first_feedback["boundary_polarity_score"], second_feedback["boundary_polarity_score"]]
    reasons = [first_response["reason_code"], second_response["reason_code"]]
    coherences = _coherences(model, role_ids)
    checks.add("private_partition.masks", masks == [[role_ids["P1_private"]], [role_ids["P2_private"]]], masks, [[role_ids["P1_private"]], [role_ids["P2_private"]]])
    checks.add("private_partition.no_common_mask", all(len(mask) == 1 for mask in masks) and not any(set(mask) == {role_ids["P1_private"], role_ids["P2_private"]} for mask in masks), masks, "two separate one-node masks")
    checks.add("private_partition.scores", scores == expected["scores"], scores, expected["scores"])
    checks.add("private_partition.reasons", reasons == expected["reason_codes"], reasons, expected["reason_codes"])
    for role, value in expected["coherences"].items():
        checks.add(f"private_partition.coherence.{role}", coherences[role] == value, coherences[role], value)
    checks.add("private_partition.queue_drained", _queue_signature(model) == [], _queue_signature(model), [])
    return {
        "branch_id": branch_id,
        "coherences": coherences,
        "one_node_reads": [
            {"partition": "P1_private", "feedback": first_feedback, "response": first_response},
            {"partition": "P2_private", "feedback": second_feedback, "response": second_response},
        ],
        "aggregation_performed": False,
        "packet_records": _packet_records(model),
        "queue_signature_after": _queue_signature(model),
        "restoration_identity_v2_after": digest_lgrc9v3_restoration_identity_v2(model),
    }


def _continuation_signature(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, Any]:
    return {
        "coherences": _coherences(model, role_ids),
        "queue_signature": _queue_signature(model),
        "packet_records": _packet_records(model),
        "restoration_identity_v2": digest_lgrc9v3_restoration_identity_v2(model),
    }


def _run_restoration(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    model, role_ids, edge_ids = _build_model(freeze)
    initial_digest = digest_lgrc9v3_restoration_identity_v2(model)
    _schedule_contributions(model, role_ids, edge_ids, freeze, freeze["fixture"]["contribution_sequences"]["combined_s1_s2"])
    _neutral_contact(model, role_ids, edge_ids, freeze)
    feedback = _prepare_feedback(model, role_ids, edge_ids, freeze)
    branch_digest = digest_lgrc9v3_restoration_identity_v2(model)
    with tempfile.TemporaryDirectory(prefix="p2-i2-i03ar1-") as directory:
        path = Path(directory) / "state.json"
        model.save(str(path))
        loaded = LGRC9V3.load(str(path))
    loaded_digest = digest_lgrc9v3_restoration_identity_v2(loaded)
    checks.add("restoration.save_load_v2", loaded_digest == branch_digest, loaded_digest, branch_digest)

    original_response = _execute_feedback(model, role_ids)
    loaded_response = _execute_feedback(loaded, role_ids)
    original_continuation = _continuation_signature(model, role_ids)
    loaded_continuation = _continuation_signature(loaded, role_ids)
    checks.add("restoration.equal_response", loaded_response == original_response, loaded_response, original_response)
    checks.add("restoration.equal_continuation", loaded_continuation == original_continuation, loaded_continuation, original_continuation)

    model.reset()
    loaded.reset()
    original_reset = _continuation_signature(model, role_ids)
    loaded_reset = _continuation_signature(loaded, role_ids)
    checks.add("restoration.equal_reset", loaded_reset == original_reset, loaded_reset, original_reset)
    checks.add("restoration.reset_v2_baseline", original_reset["restoration_identity_v2"] == initial_digest, original_reset["restoration_identity_v2"], initial_digest)
    checks.add("restoration.reset_pool", original_reset["coherences"]["P"] == 1.0, original_reset["coherences"]["P"], 1.0)
    checks.add("restoration.reset_queue", original_reset["queue_signature"] == [], original_reset["queue_signature"], [])
    checks.add("restoration.reset_packets", original_reset["packet_records"] == [], original_reset["packet_records"], [])
    return {
        "branch_id": "restoration_continuation",
        "feedback_before_save": feedback,
        "initial_restoration_identity_v2": initial_digest,
        "pre_save_restoration_identity_v2": branch_digest,
        "loaded_restoration_identity_v2": loaded_digest,
        "original_response": original_response,
        "loaded_response": loaded_response,
        "original_continuation": original_continuation,
        "loaded_continuation": loaded_continuation,
        "original_reset": original_reset,
        "loaded_reset": loaded_reset,
    }


def _causal_signature(branch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "pool": branch["coherences"]["P"],
        "score": branch["feedback"]["boundary_polarity_score"],
        "reason_code": branch["response"]["reason_code"],
        "scheduled": branch["response"]["scheduled"],
        "response_delta": branch["response"]["target_coherence_after"] - branch["response"]["target_coherence_before"],
    }


def _source_lineages(branch: Mapping[str, Any]) -> list[list[Any]]:
    return [
        [row["source_node_id"], row["source_lineage_id"]]
        for row in branch["packet_records"]
        if row["source_node_id"] in {0, 1}
    ]


def _run_conformance(freeze: Mapping[str, Any], runtime_receipt: dict[str, Any]) -> dict[str, Any]:
    checks = Checks()
    branches: dict[str, Any] = {}
    for branch_id, contribution_key in (
        ("reference", None),
        ("s1_only", "s1_only"),
        ("s2_only", "s2_only"),
        ("combined_s1_s2", "combined_s1_s2"),
        ("combined_s2_s1", "combined_s2_s1"),
        ("lineage_permuted", "lineage_permuted"),
        ("write_diversion", "write_diversion"),
    ):
        branches[branch_id] = _run_standard_branch(branch_id, freeze, contribution_key, checks)
    branches["carrier_debit"] = _run_carrier_debit(freeze, checks)
    branches["private_partition"] = _run_private_partition(freeze, checks)
    branches["alternate_responder"] = _run_standard_branch(
        "alternate_responder",
        freeze,
        "combined_s1_s2",
        checks,
        response_source="A_alt",
        response_target="B_alt",
        response_edge="A_alt_to_B_alt",
    )
    branches["restoration_continuation"] = _run_restoration(freeze, checks)

    combined = branches["combined_s1_s2"]
    reversed_order = branches["combined_s2_s1"]
    permuted = branches["lineage_permuted"]
    diversion = branches["write_diversion"]
    debit = branches["carrier_debit"]
    alternate = branches["alternate_responder"]
    checks.add("cross.order_invariance", _causal_signature(reversed_order) == _causal_signature(combined), _causal_signature(reversed_order), _causal_signature(combined))
    checks.add("cross.lineage_causal_invariance", _causal_signature(permuted) == _causal_signature(combined), _causal_signature(permuted), _causal_signature(combined))
    checks.add("cross.lineage_audit_changed", _source_lineages(permuted) != _source_lineages(combined), _source_lineages(permuted), "different from canonical source lineage assignment")
    checks.add("cross.diversion_source_debits", [diversion["coherences"]["S1"], diversion["coherences"]["S2"]] == [combined["coherences"]["S1"], combined["coherences"]["S2"]], [diversion["coherences"]["S1"], diversion["coherences"]["S2"]], [combined["coherences"]["S1"], combined["coherences"]["S2"]])
    checks.add("cross.debit_source_debits", [debit["coherences"]["S1"], debit["coherences"]["S2"]] == [combined["coherences"]["S1"], combined["coherences"]["S2"]], [debit["coherences"]["S1"], debit["coherences"]["S2"]], [combined["coherences"]["S1"], combined["coherences"]["S2"]])
    checks.add("cross.alternate_same_pool_read", alternate["feedback"]["front_node_ids"] == combined["feedback"]["front_node_ids"] and alternate["feedback"]["rear_node_ids"] == combined["feedback"]["rear_node_ids"], {"front": alternate["feedback"]["front_node_ids"], "rear": alternate["feedback"]["rear_node_ids"]}, {"front": combined["feedback"]["front_node_ids"], "rear": combined["feedback"]["rear_node_ids"]})
    checks.add("cross.alternate_same_relation", _causal_signature(alternate) == _causal_signature(combined), _causal_signature(alternate), _causal_signature(combined))

    graph_after = _graph_guard()
    checks.add("guard.graph_revision_unchanged", graph_after["revision"] == runtime_receipt["graph_before"]["revision"], graph_after["revision"], runtime_receipt["graph_before"]["revision"])
    checks.add("guard.graph_clean_after", graph_after["status_porcelain"] == "", graph_after["status_porcelain"], "")
    for path, before_digest in runtime_receipt["graph_source_digests"].items():
        checks.add(f"guard.source_unchanged:{path}", _sha256(GRAPH_ROOT / path) == before_digest, _sha256(GRAPH_ROOT / path), before_digest)
    runtime_receipt["graph_after"] = graph_after

    return {
        "artifact_id": "P2-I2-I03AR1-STATE-CARRIED-RUNTIME-CONFORMANCE",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03AR1",
        "pool_dependence_mode": "state_carried",
        "status": "runtime_conformant",
        "evidence_class": "quarantined_realization_implementation_conformance",
        "scientific_evidence_assigned": False,
        "runtime_receipt": runtime_receipt,
        "run_policy": freeze["run_policy"],
        "quarantine": freeze["quarantine"],
        "fixture_id": freeze["fixture"]["fixture_id"],
        "branches": branches,
        "assertions": checks.rows,
        "assertion_summary": {
            "total": len(checks.rows),
            "passed": sum(1 for row in checks.rows if row["passed"]),
            "failed": sum(1 for row in checks.rows if not row["passed"]),
        },
        "disposition": "state_carried_native_candidate_runtime_conformant_pending_owner_review",
        "next_iteration_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-freeze-only", action="store_true")
    args = parser.parse_args()
    freeze_path = args.freeze.resolve()
    freeze = _resolve_freeze(freeze_path)
    receipt = _validate_freeze(freeze, freeze_path)
    if args.validate_freeze_only:
        print(json.dumps({"status": "freeze_valid", "runtime_operation_performed": False, "runtime_receipt": receipt}, indent=2, sort_keys=True))
        return 0
    _require(args.output is not None, "--output is required for runtime conformance")
    record = _run_conformance(freeze, receipt)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical_json_bytes(record))
    print(json.dumps({"status": record["status"], "assertion_summary": record["assertion_summary"], "output": str(output), "sha256": _sha256(output)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
