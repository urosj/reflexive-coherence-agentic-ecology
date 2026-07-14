#!/usr/bin/env python3
"""Frozen P2-I2-I03B history-carried implementation-conformance harness.

The output is quarantined implementation evidence. It must not be used for
I04/I05 calibration, I06 registration, I08 scientific execution, mode
ranking, or an AE01-H-L02 conclusion.
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
    LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS,
    PortEdge,
    digest_lgrc9v3_restoration_identity_v2,
    lgrc9v3_restoration_identity_v2,
)

from p2_i2_i03b_history_adapter import (
    RCAEActiveHistoryAdapterV1,
    TOKEN_FIELDS,
    digest_canonical,
)


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = Path("/home/uros/Documents/RC-github/graph-reflexive-coherence")
GRAPH_SOURCE_ROOT = GRAPH_ROOT / "src"
SCRIPT_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03b_conform.py"
)
ADAPTER_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03b_history_adapter.py"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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
    _require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def _close(observed: float, expected: float, freeze: Mapping[str, Any]) -> bool:
    comparator = freeze["assertions"]["float_comparator"]
    return math.isclose(
        float(observed),
        float(expected),
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
        _require(
            condition,
            f"{check_id} failed: observed={observed!r} expected={expected!r}",
        )


class ScheduleCursor:
    """Deterministic fixture-only native packet slot allocator."""

    def __init__(self) -> None:
        self.next_departure_event_time_key = 1.0
        self.next_scheduler_event_index = 1
        self.next_packet_index = 0

    def take(self) -> dict[str, Any]:
        result = {
            "departure_event_time_key": self.next_departure_event_time_key,
            "arrival_event_time_key": self.next_departure_event_time_key + 1.0,
            "scheduler_event_index": self.next_scheduler_event_index,
            "packet_index": self.next_packet_index,
        }
        self.next_departure_event_time_key += 2.0
        self.next_scheduler_event_index += 2
        self.next_packet_index += 1
        return result


def _validate_freeze(freeze: Mapping[str, Any], freeze_path: Path) -> dict[str, Any]:
    _require(
        freeze.get("artifact_id")
        == "P2-I2-I03B-HISTORY-CARRIED-RUNTIME-CONFORMANCE-INPUT-FREEZE",
        "wrong freeze artifact_id",
    )
    _require(freeze.get("iteration_id") == "P2-I2-I03B", "wrong iteration_id")
    _require(
        freeze.get("pool_dependence_mode") == "history_carried",
        "wrong dependence mode",
    )
    _require(freeze.get("runtime_authorized") is True, "runtime not authorized")
    run_policy = freeze["run_policy"]
    _require(run_policy["evidence_invocations"] == 1, "evidence count must be one")
    _require(
        run_policy["reconstruction_invocations"] == 1,
        "reconstruction count must be one",
    )
    _require(run_policy["retry_limit"] == 0, "retry limit must be zero")
    _require(run_policy["parameter_search_allowed"] is False, "search prohibited")
    _require(run_policy["rescue_variants_allowed"] is False, "rescue prohibited")
    _require(
        run_policy["branch_scenarios_per_invocation"] == 12,
        "wrong branch count",
    )

    authority = freeze["authority"]
    for item in authority["bound_rcae_artifacts"]:
        path = ROOT / item["path"]
        _require(path.is_file(), f"missing bound RCAE artifact: {path}")
        _require(_sha256(path) == item["sha256"], f"RCAE digest mismatch: {path}")

    harness = authority["harness"]
    harness_path = ROOT / harness["path"]
    _require(harness_path.resolve() == Path(__file__).resolve(), "wrong harness path")
    _require(_sha256(harness_path) == harness["sha256"], "harness digest mismatch")
    adapter = authority["adapter"]
    adapter_path = ROOT / adapter["path"]
    _require(
        adapter_path.resolve() == (ROOT / ADAPTER_RELATIVE_PATH).resolve(),
        "wrong adapter path",
    )
    _require(_sha256(adapter_path) == adapter["sha256"], "adapter digest mismatch")

    graph_before = _graph_guard()
    _require(graph_before["revision"] == authority["graph_revision"], "graph mismatch")
    _require(graph_before["status_porcelain"] == "", "graph checkout not clean")
    source_digests: dict[str, str] = {}
    for item in authority["bound_graph_sources"]:
        path = GRAPH_ROOT / item["path"]
        _require(path.is_file(), f"missing graph source: {path}")
        actual = _sha256(path)
        _require(actual == item["sha256"], f"graph source digest mismatch: {path}")
        source_digests[item["path"]] = actual

    expected_import = (GRAPH_SOURCE_ROOT / "pygrc" / "__init__.py").resolve()
    actual_import = Path(pygrc.__file__).resolve()
    _require(actual_import == expected_import, "PyGRC import outside admitted checkout")
    environment = freeze["environment"]
    _require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "RCAE .venv inactive")
    versions = {
        name: importlib.metadata.version(name)
        for name in environment["direct_dependencies"]
    }
    _require(versions == environment["direct_dependencies"], "dependency mismatch")
    _require(platform.python_version() == environment["python_version"], "Python mismatch")
    _require(
        any(Path(item).resolve() == GRAPH_SOURCE_ROOT.resolve() for item in sys.path if item),
        "admitted graph source root absent from sys.path",
    )

    return {
        "freeze_path": str(freeze_path.relative_to(ROOT)),
        "freeze_sha256": _sha256(freeze_path),
        "harness_path": SCRIPT_RELATIVE_PATH,
        "harness_sha256": _sha256(Path(__file__)),
        "adapter_path": ADAPTER_RELATIVE_PATH,
        "adapter_sha256": _sha256(ROOT / ADAPTER_RELATIVE_PATH),
        "graph_before": graph_before,
        "graph_source_digests": source_digests,
        "pygrc_import_file": str(actual_import),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "sys_executable": sys.executable,
        "sys_prefix": sys.prefix,
        "direct_dependency_versions": versions,
    }


def _build_model(
    freeze: Mapping[str, Any],
) -> tuple[LGRC9V3, dict[str, int], dict[str, int]]:
    fixture = freeze["fixture"]
    graph = PortGraphBackend()
    role_ids: dict[str, int] = {}
    for node in fixture["nodes"]:
        node_id = graph.add_node({"label": node["role"]})
        _require(node_id == node["node_id"], f"node id mismatch: {node['role']}")
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
        _require(edge_id == edge["edge_id"], f"edge id mismatch: {edge['edge_role']}")
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
        role_ids[node["role"]]: GRC9V3NodeState(
            coherence=float(node["initial_coherence"])
        )
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
            "proper_time_accumulation_policy": modes[
                "proper_time_accumulation_policy"
            ],
            "causal_pulse_substrate_surface_enabled": True,
            "causal_pulse_substrate_surface_policy": (
                LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS
            ),
            "causal_pulse_substrate_surface_validated": False,
        },
    }
    return LGRC9V3.from_state(state, params), role_ids, edge_ids


def _adapter(
    freeze: Mapping[str, Any],
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    *,
    profile: str = "common",
) -> RCAEActiveHistoryAdapterV1:
    config = freeze["fixture"]["adapter_profiles"][profile]
    return RCAEActiveHistoryAdapterV1(
        carrier_id=str(config["carrier_id"]),
        pool_target_node_id=role_ids[str(config["pool_target_role"])],
        registered_source_node_ids=[
            role_ids[str(role)] for role in config["registered_source_roles"]
        ],
        readout_node_id=role_ids[str(config["readout_role"])],
        positive_reservoir_node_id=role_ids[str(config["positive_reservoir_role"])],
        negative_sink_node_id=role_ids[str(config["negative_sink_role"])],
        positive_edge_id=edge_ids[str(config["positive_edge_role"])],
        negative_edge_id=edge_ids[str(config["negative_edge_role"])],
        recency_coefficient=float(config["recency_coefficient"]),
    )


def _drain(model: LGRC9V3, count: int) -> None:
    for _ in range(count):
        _require(
            bool(model.get_state().packet_ledger.event_queue_records),
            "native queue drained before frozen count",
        )
        model.step()
    _require(
        not model.get_state().packet_ledger.event_queue_records,
        "native queue not drained after frozen count",
    )


def _schedule_and_drain(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: ScheduleCursor,
    *,
    source: str,
    target: str,
    edge_role: str,
    amount: float,
    source_lineage_id: str,
    target_lineage_id: str,
) -> dict[str, Any]:
    spec = cursor.take()
    model.schedule_packet_departure(
        source_node_id=role_ids[source],
        target_node_id=role_ids[target],
        edge_id=edge_ids[edge_role],
        amount=float(amount),
        departure_event_time_key=spec["departure_event_time_key"],
        arrival_event_time_key=spec["arrival_event_time_key"],
        scheduler_event_index=spec["scheduler_event_index"],
        packet_index=spec["packet_index"],
        source_lineage_id=source_lineage_id,
        target_lineage_id=target_lineage_id,
    )
    _drain(model, 2)
    return spec


def _schedule_contributions(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: ScheduleCursor,
    specs: Sequence[Mapping[str, Any]],
) -> None:
    for spec in specs:
        _schedule_and_drain(
            model,
            role_ids,
            edge_ids,
            cursor,
            source=str(spec["source"]),
            target=str(spec["target"]),
            edge_role=str(spec["edge_role"]),
            amount=float(spec["amount"]),
            source_lineage_id=str(spec["source_lineage_id"]),
            target_lineage_id=str(spec["target_lineage_id"]),
        )


def _materialize(
    adapter: RCAEActiveHistoryAdapterV1,
    model: LGRC9V3,
    cursor: ScheduleCursor,
) -> dict[str, Any]:
    return adapter.materialize_readout(model, **cursor.take())


def _neutral_contact(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: ScheduleCursor,
    freeze: Mapping[str, Any],
) -> None:
    spec = freeze["fixture"]["neutral_contact"]
    _schedule_and_drain(
        model,
        role_ids,
        edge_ids,
        cursor,
        source=str(spec["source"]),
        target=str(spec["target"]),
        edge_role=str(spec["edge_role"]),
        amount=float(spec["amount"]),
        source_lineage_id=str(spec["source_lineage_id"]),
        target_lineage_id=str(spec["target_lineage_id"]),
    )


def _prepare_feedback(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: ScheduleCursor,
    freeze: Mapping[str, Any],
    *,
    front_role: str = "M_H",
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
) -> dict[str, Any]:
    config = freeze["fixture"]["response"]
    row = model.emit_feedback_eligibility_surface_row(
        front_node_ids=(role_ids[front_role],),
        rear_node_ids=(role_ids["B_ref"],),
        reference_delta=float(config["reference_delta"]),
        feedback_threshold=float(config["threshold"]),
    )
    response_slot = cursor.take()
    model.set_feedback_coupled_pulse_producer(
        source_node_id=role_ids[response_source],
        target_node_id=role_ids[response_target],
        edge_id=edge_ids[response_edge],
        threshold=float(config["threshold"]),
        packet_amount=float(config["packet_amount"]),
        expected_polarity=str(config["expected_polarity"]),
        expected_source_surface_digest=None,
        arrival_event_time_key=float(response_slot["arrival_event_time_key"]),
    )
    return {
        "surface_digest": row.surface_digest,
        "front_node_ids": list(row.surface_update_policy["declared_front_node_ids"]),
        "rear_node_ids": list(row.surface_update_policy["declared_rear_node_ids"]),
        "front_mass": float(row.surface_values_after["front_mass"]),
        "rear_mass": float(row.surface_values_after["rear_mass"]),
        "boundary_polarity_score": float(
            row.surface_values_after["boundary_polarity_score"]
        ),
        "expected_source_surface_digest": None,
        "response_slot": response_slot,
    }


def _execute_feedback(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    *,
    response_target: str = "B",
) -> dict[str, Any]:
    before = float(model.get_state().base_state.nodes[role_ids[response_target]].coherence)
    result = model.produce_events(
        policy=(
            LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY
        )
    )
    _require(len(result.production_records) == 1, "expected one producer record")
    record = result.production_records[0]
    scheduled = record.reason_code == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED
    if scheduled:
        _drain(model, 2)
    else:
        _require(
            not model.get_state().packet_ledger.event_queue_records,
            "negative feedback enqueued native work",
        )
    after = float(model.get_state().base_state.nodes[role_ids[response_target]].coherence)
    return {
        "reason_code": record.reason_code,
        "scheduled": scheduled,
        "target_coherence_before": before,
        "target_coherence_after": after,
        "response_delta": after - before,
        "producer_mutated_coherence": bool(
            record.observed_evidence.get("producer_mutated_coherence", False)
        ),
        "direct_claim_write": bool(
            record.observed_evidence.get("direct_claim_write", False)
        ),
        "threshold_source": record.observed_evidence.get("threshold_source"),
        "polarity_policy_source": record.observed_evidence.get(
            "polarity_policy_source"
        ),
    }


def _coherences(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, float]:
    nodes = model.get_state().base_state.nodes
    return {
        role: float(nodes[node_id].coherence)
        for role, node_id in sorted(role_ids.items())
    }


def _packet_records(model: LGRC9V3) -> list[dict[str, Any]]:
    return [row.to_record() for row in model.get_state().packet_ledger.packet_records]


def _surface_rows(model: LGRC9V3) -> list[dict[str, Any]]:
    return [row.to_artifact() for row in model.get_state().causal_pulse_substrate_surface_log]


def _token_amounts(adapter: RCAEActiveHistoryAdapterV1) -> list[float]:
    return [float(token["contact_amount"]) for token in adapter.tokens]


def _tokens_have_only_frozen_fields(adapter: RCAEActiveHistoryAdapterV1) -> bool:
    return all(set(token) == set(TOKEN_FIELDS) for token in adapter.tokens)


def _source_lineages(model: LGRC9V3, source_ids: set[int]) -> list[list[Any]]:
    return [
        [row["source_node_id"], row["source_lineage_id"]]
        for row in _packet_records(model)
        if row["source_node_id"] in source_ids
    ]


def _composite_artifact(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_kind": "p2_i2_i03b_composite_restoration_identity",
        "artifact_schema_version": "p2_i2_i03b_composite_restoration_identity_v1",
        "fixture_id": freeze["fixture"]["fixture_id"],
        "native_restoration_identity_v2": lgrc9v3_restoration_identity_v2(model),
        "adapter_restoration_identity": adapter.restoration_identity_artifact(),
        "binding": freeze["fixture"]["composite_identity_binding"],
    }


def _composite_summary(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    freeze: Mapping[str, Any],
) -> dict[str, str]:
    artifact = _composite_artifact(model, adapter, freeze)
    return {
        "composite_digest": digest_canonical(artifact),
        "native_v2_digest": digest_lgrc9v3_restoration_identity_v2(model),
        "adapter_restoration_digest": adapter.restoration_identity_digest(),
        "binding_digest": digest_canonical(freeze["fixture"]["composite_identity_binding"]),
    }


def _assert_standard_branch(
    branch_id: str,
    expected: Mapping[str, Any],
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    materialization: Mapping[str, Any],
    feedback: Mapping[str, Any],
    response: Mapping[str, Any],
    role_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
    checks: Checks,
) -> None:
    amounts = _token_amounts(adapter)
    coherences = _coherences(model, role_ids)
    checks.add(f"{branch_id}.token_amounts", amounts == expected["token_amounts"], amounts, expected["token_amounts"])
    checks.add(f"{branch_id}.token_schema", _tokens_have_only_frozen_fields(adapter), [sorted(token) for token in adapter.tokens], sorted(TOKEN_FIELDS))
    checks.add(f"{branch_id}.readout", _close(adapter.readout(), expected["readout"], freeze), adapter.readout(), expected["readout"])
    checks.add(f"{branch_id}.materialized_readout", _close(materialization["readout_after"], expected["readout"], freeze), materialization["readout_after"], expected["readout"])
    checks.add(f"{branch_id}.adapter_no_success", materialization["success_or_response_computed"] is False and materialization["later_response_scheduled"] is False, {"computed": materialization["success_or_response_computed"], "scheduled": materialization["later_response_scheduled"]}, {"computed": False, "scheduled": False})
    checks.add(f"{branch_id}.adapter_no_direct_native_write", materialization["direct_native_state_mutation"] is False, materialization["direct_native_state_mutation"], False)
    checks.add(f"{branch_id}.front_mask", feedback["front_node_ids"] == [role_ids[expected.get("front_role", "M_H")]], feedback["front_node_ids"], [role_ids[expected.get("front_role", "M_H")]])
    checks.add(f"{branch_id}.front_excludes_P", role_ids["P"] not in feedback["front_node_ids"], feedback["front_node_ids"], "P absent")
    checks.add(f"{branch_id}.expected_digest_null", feedback["expected_source_surface_digest"] is None, feedback["expected_source_surface_digest"], None)
    checks.add(f"{branch_id}.score", _close(feedback["boundary_polarity_score"], expected["score"], freeze), feedback["boundary_polarity_score"], expected["score"])
    checks.add(f"{branch_id}.reason", response["reason_code"] == expected["reason_code"], response["reason_code"], expected["reason_code"])
    checks.add(f"{branch_id}.scheduled", response["scheduled"] is expected["scheduled"], response["scheduled"], expected["scheduled"])
    checks.add(f"{branch_id}.response_delta", _close(response["response_delta"], expected["response_delta"], freeze), response["response_delta"], expected["response_delta"])
    checks.add(f"{branch_id}.native_producer_no_direct_coherence", response["producer_mutated_coherence"] is False, response["producer_mutated_coherence"], False)
    checks.add(f"{branch_id}.native_producer_no_claim", response["direct_claim_write"] is False, response["direct_claim_write"], False)
    for role, value in expected["coherences"].items():
        checks.add(f"{branch_id}.coherence.{role}", _close(coherences[role], value, freeze), coherences[role], value)
    checks.add(f"{branch_id}.queue_drained", not model.get_state().packet_ledger.event_queue_records, len(model.get_state().packet_ledger.event_queue_records), 0)


def _run_standard_branch(
    branch_id: str,
    freeze: Mapping[str, Any],
    checks: Checks,
    *,
    contribution_key: str,
    adapter_profile: str = "common",
    front_role: str = "M_H",
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
    state_debit: bool = False,
    history_clamp: bool = False,
) -> dict[str, Any]:
    model, role_ids, edge_ids = _build_model(freeze)
    adapter = _adapter(freeze, role_ids, edge_ids, profile=adapter_profile)
    cursor = ScheduleCursor()
    specs = freeze["fixture"]["contribution_sequences"][contribution_key]
    _schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    appended = adapter.ingest_new_rows(model)
    first_materialization = _materialize(adapter, model, cursor)
    intervention = None
    if history_clamp:
        intervention = adapter.replace_history(
            (),
            intervention_id="i03b-conformance-clamp-to-reference",
            reason="fixture-only history clamp with native contribution audit preserved",
        )
        materialization = _materialize(adapter, model, cursor)
    else:
        materialization = first_materialization
    state_debit_record = None
    if state_debit:
        debit = freeze["fixture"]["state_only_debit"]
        slot = _schedule_and_drain(
            model,
            role_ids,
            edge_ids,
            cursor,
            source=str(debit["source"]),
            target=str(debit["target"]),
            edge_role=str(debit["edge_role"]),
            amount=float(debit["amount"]),
            source_lineage_id=str(debit["source_lineage_id"]),
            target_lineage_id=str(debit["target_lineage_id"]),
        )
        state_debit_record = {**debit, **slot}
    _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        cursor,
        freeze,
        front_role=front_role,
        response_source=response_source,
        response_target=response_target,
        response_edge=response_edge,
    )
    response = _execute_feedback(model, role_ids, response_target=response_target)
    expected = freeze["assertions"]["branches"][branch_id]
    _assert_standard_branch(
        branch_id,
        expected,
        model,
        adapter,
        materialization,
        feedback,
        response,
        role_ids,
        freeze,
        checks,
    )
    if history_clamp:
        checks.add("active_history_clamp.intervention_explicit", intervention is not None and intervention["native_audit_rewritten"] is False and intervention["success_or_response_written"] is False, intervention, "explicit external intervention without audit/success rewrite")
        checks.add("active_history_clamp.P_preserved", _close(_coherences(model, role_ids)["P"], 1.6, freeze), _coherences(model, role_ids)["P"], 1.6)
    if state_debit:
        checks.add("state_only.H_preserved", _token_amounts(adapter) == [0.2, 0.4], _token_amounts(adapter), [0.2, 0.4])
        checks.add("state_only.M_preserved", _close(_coherences(model, role_ids)["M_H"], 0.5, freeze), _coherences(model, role_ids)["M_H"], 0.5)
    return {
        "branch_id": branch_id,
        "tokens": list(adapter.tokens),
        "adapter_current_identity_digest": adapter.current_identity_digest(),
        "adapter_restoration_identity_digest": adapter.restoration_identity_digest(),
        "appended_tokens": list(appended),
        "first_materialization": first_materialization,
        "final_materialization": materialization,
        "history_intervention": intervention,
        "state_debit": state_debit_record,
        "coherences": _coherences(model, role_ids),
        "feedback": feedback,
        "response": response,
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
        "source_lineages": _source_lineages(model, {role_ids["S1"], role_ids["S2"]}),
        "composite_identity": _composite_summary(model, adapter, freeze),
    }


def _run_private_partition(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    branch_id = "private_partition"
    model, role_ids, edge_ids = _build_model(freeze)
    h1 = _adapter(freeze, role_ids, edge_ids, profile="private_one")
    h2 = _adapter(freeze, role_ids, edge_ids, profile="private_two")
    cursor = ScheduleCursor()
    specs = freeze["fixture"]["contribution_sequences"]["combined_q1_q2"]
    _schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    h1_appended = h1.ingest_new_rows(model)
    h2_appended = h2.ingest_new_rows(model)
    h1_materialization = _materialize(h1, model, cursor)
    h2_materialization = _materialize(h2, model, cursor)
    _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    first_feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        cursor,
        freeze,
        front_role="M_H1",
    )
    first_response = _execute_feedback(model, role_ids)
    second_feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        cursor,
        freeze,
        front_role="M_H2",
        response_source="A_alt",
        response_target="B_alt",
        response_edge="A_alt_to_B_alt",
    )
    second_response = _execute_feedback(model, role_ids, response_target="B_alt")
    expected = freeze["assertions"]["branches"][branch_id]
    masks = [first_feedback["front_node_ids"], second_feedback["front_node_ids"]]
    scores = [
        first_feedback["boundary_polarity_score"],
        second_feedback["boundary_polarity_score"],
    ]
    reasons = [first_response["reason_code"], second_response["reason_code"]]
    checks.add("private.token_amounts", [_token_amounts(h1), _token_amounts(h2)] == expected["token_amounts"], [_token_amounts(h1), _token_amounts(h2)], expected["token_amounts"])
    checks.add("private.token_schema", _tokens_have_only_frozen_fields(h1) and _tokens_have_only_frozen_fields(h2), [list(h1.tokens), list(h2.tokens)], "only frozen non-source token fields")
    checks.add("private.one_node_masks", masks == [[role_ids["M_H1"]], [role_ids["M_H2"]]], masks, [[role_ids["M_H1"]], [role_ids["M_H2"]]])
    checks.add("private.no_common_read", all(len(mask) == 1 for mask in masks) and not any(set(mask) == {role_ids["M_H1"], role_ids["M_H2"]} for mask in masks), masks, "two separate one-node reads")
    checks.add("private.scores", all(_close(observed, target, freeze) for observed, target in zip(scores, expected["scores"], strict=True)), scores, expected["scores"])
    checks.add("private.reasons", reasons == expected["reason_codes"], reasons, expected["reason_codes"])
    checks.add("private.no_responses", first_response["scheduled"] is False and second_response["scheduled"] is False, [first_response["scheduled"], second_response["scheduled"]], [False, False])
    checks.add("private.adapter_no_success", h1_materialization["success_or_response_computed"] is False and h2_materialization["success_or_response_computed"] is False, [h1_materialization["success_or_response_computed"], h2_materialization["success_or_response_computed"]], [False, False])
    checks.add("private.P_matched", _close(_coherences(model, role_ids)["P"], 1.6, freeze), _coherences(model, role_ids)["P"], 1.6)
    return {
        "branch_id": branch_id,
        "private_histories": [
            {
                "carrier_id": h1.carrier_id,
                "tokens": list(h1.tokens),
                "appended_tokens": list(h1_appended),
                "materialization": h1_materialization,
                "feedback": first_feedback,
                "response": first_response,
            },
            {
                "carrier_id": h2.carrier_id,
                "tokens": list(h2.tokens),
                "appended_tokens": list(h2_appended),
                "materialization": h2_materialization,
                "feedback": second_feedback,
                "response": second_response,
            },
        ],
        "aggregation_performed": False,
        "coherences": _coherences(model, role_ids),
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
    }


def _continuation_signature(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    role_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "coherences": _coherences(model, role_ids),
        "tokens": list(adapter.tokens),
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
        "queue_length": len(model.get_state().packet_ledger.event_queue_records),
        "composite_identity": _composite_summary(model, adapter, freeze),
    }


def _prepare_restoration_branch(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    freeze: Mapping[str, Any],
    cursor: ScheduleCursor,
) -> dict[str, Any]:
    specs = freeze["fixture"]["contribution_sequences"]["combined_q1_q2"]
    _schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    adapter.ingest_new_rows(model)
    materialization = _materialize(adapter, model, cursor)
    _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    feedback = _prepare_feedback(model, role_ids, edge_ids, cursor, freeze)
    return {"materialization": materialization, "feedback": feedback}


def _run_restoration(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    model, role_ids, edge_ids = _build_model(freeze)
    adapter = _adapter(freeze, role_ids, edge_ids)
    initial = _composite_summary(model, adapter, freeze)
    cursor = ScheduleCursor()
    prepared = _prepare_restoration_branch(
        model,
        adapter,
        role_ids,
        edge_ids,
        freeze,
        cursor,
    )
    pre_save = _composite_summary(model, adapter, freeze)
    with tempfile.TemporaryDirectory(prefix="p2-i2-i03b-") as directory:
        root = Path(directory)
        native_path = root / "native.json"
        adapter_path = root / "adapter.json"
        manifest_path = root / "manifest.json"
        model.save(str(native_path))
        adapter.save(adapter_path)
        manifest = {
            "artifact_kind": "p2_i2_i03b_paired_save_manifest",
            "artifact_schema_version": "p2_i2_i03b_paired_save_manifest_v1",
            "native_snapshot_sha256": _sha256(native_path),
            "adapter_snapshot_sha256": _sha256(adapter_path),
            "composite_identity_before_save": pre_save,
        }
        manifest_path.write_bytes(_canonical_json_bytes(manifest))
        loaded_model = LGRC9V3.load(str(native_path))
        loaded_adapter = RCAEActiveHistoryAdapterV1.load(adapter_path)
        retained_manifest = _load_json(manifest_path)
    loaded = _composite_summary(loaded_model, loaded_adapter, freeze)
    checks.add("restoration.paired_load_identity", loaded == pre_save, loaded, pre_save)
    checks.add("restoration.manifest_composite", retained_manifest["composite_identity_before_save"] == pre_save, retained_manifest["composite_identity_before_save"], pre_save)

    original_response = _execute_feedback(model, role_ids)
    loaded_response = _execute_feedback(loaded_model, role_ids)
    original_after_response = _continuation_signature(model, adapter, role_ids, freeze)
    loaded_after_response = _continuation_signature(loaded_model, loaded_adapter, role_ids, freeze)
    checks.add("restoration.equal_response", loaded_response == original_response, loaded_response, original_response)
    checks.add("restoration.equal_post_response_continuation", loaded_after_response == original_after_response, loaded_after_response, original_after_response)

    model.reset()
    adapter.reset()
    loaded_model.reset()
    loaded_adapter.reset()
    original_reset = _continuation_signature(model, adapter, role_ids, freeze)
    loaded_reset = _continuation_signature(loaded_model, loaded_adapter, role_ids, freeze)
    checks.add("restoration.equal_paired_reset", loaded_reset == original_reset, loaded_reset, original_reset)
    checks.add("restoration.reset_matches_initial", original_reset["composite_identity"] == initial, original_reset["composite_identity"], initial)
    checks.add("restoration.reset_history_empty", original_reset["tokens"] == [], original_reset["tokens"], [])
    checks.add("restoration.reset_queue_empty", original_reset["queue_length"] == 0, original_reset["queue_length"], 0)

    original_cursor = ScheduleCursor()
    loaded_cursor = ScheduleCursor()
    q1_spec = freeze["fixture"]["contribution_sequences"]["q1_only"]
    _schedule_contributions(model, role_ids, edge_ids, original_cursor, q1_spec)
    _schedule_contributions(loaded_model, role_ids, edge_ids, loaded_cursor, q1_spec)
    adapter.ingest_new_rows(model)
    loaded_adapter.ingest_new_rows(loaded_model)
    _materialize(adapter, model, original_cursor)
    _materialize(loaded_adapter, loaded_model, loaded_cursor)
    _neutral_contact(model, role_ids, edge_ids, original_cursor, freeze)
    _neutral_contact(loaded_model, role_ids, edge_ids, loaded_cursor, freeze)
    original_feedback = _prepare_feedback(
        model, role_ids, edge_ids, original_cursor, freeze
    )
    loaded_feedback = _prepare_feedback(
        loaded_model, role_ids, edge_ids, loaded_cursor, freeze
    )
    original_continuation_response = _execute_feedback(model, role_ids)
    loaded_continuation_response = _execute_feedback(loaded_model, role_ids)
    original_continuation = _continuation_signature(model, adapter, role_ids, freeze)
    loaded_continuation = _continuation_signature(
        loaded_model, loaded_adapter, role_ids, freeze
    )
    checks.add("restoration.equal_reset_input_feedback", loaded_feedback == original_feedback, loaded_feedback, original_feedback)
    checks.add("restoration.equal_reset_input_response", loaded_continuation_response == original_continuation_response, loaded_continuation_response, original_continuation_response)
    checks.add("restoration.equal_reset_input_continuation", loaded_continuation == original_continuation, loaded_continuation, original_continuation)
    return {
        "branch_id": "restoration_continuation",
        "initial_composite_identity": initial,
        "prepared_before_save": prepared,
        "pre_save_composite_identity": pre_save,
        "paired_save_manifest": retained_manifest,
        "loaded_composite_identity": loaded,
        "original_response": original_response,
        "loaded_response": loaded_response,
        "original_after_response": original_after_response,
        "loaded_after_response": loaded_after_response,
        "original_reset": original_reset,
        "loaded_reset": loaded_reset,
        "original_reset_continuation": original_continuation,
        "loaded_reset_continuation": loaded_continuation,
    }


def _causal_signature(branch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "token_amounts": [token["contact_amount"] for token in branch["tokens"]],
        "readout": branch["final_materialization"]["readout_after"],
        "P": branch["coherences"]["P"],
        "M_H": branch["coherences"]["M_H"],
        "score": branch["feedback"]["boundary_polarity_score"],
        "reason_code": branch["response"]["reason_code"],
        "scheduled": branch["response"]["scheduled"],
        "response_delta": branch["response"]["response_delta"],
    }


def _run_conformance(
    freeze: Mapping[str, Any], runtime_receipt: dict[str, Any]
) -> dict[str, Any]:
    checks = Checks()
    branches: dict[str, Any] = {}
    for branch_id, contribution_key in (
        ("reference", "reference"),
        ("q1_only", "q1_only"),
        ("q2_only", "q2_only"),
        ("combined_q1_q2", "combined_q1_q2"),
        ("combined_q2_q1", "combined_q2_q1"),
        ("lineage_permuted", "lineage_permuted"),
        ("write_diversion", "write_diversion"),
    ):
        branches[branch_id] = _run_standard_branch(
            branch_id,
            freeze,
            checks,
            contribution_key=contribution_key,
        )
    branches["active_history_clamp"] = _run_standard_branch(
        "active_history_clamp",
        freeze,
        checks,
        contribution_key="combined_q1_q2",
        history_clamp=True,
    )
    branches["state_only_separation"] = _run_standard_branch(
        "state_only_separation",
        freeze,
        checks,
        contribution_key="combined_q1_q2",
        state_debit=True,
    )
    branches["private_partition"] = _run_private_partition(freeze, checks)
    branches["alternate_responder"] = _run_standard_branch(
        "alternate_responder",
        freeze,
        checks,
        contribution_key="combined_q1_q2",
        response_source="A_alt",
        response_target="B_alt",
        response_edge="A_alt_to_B_alt",
    )
    branches["restoration_continuation"] = _run_restoration(freeze, checks)

    canonical = branches["combined_q1_q2"]
    reversed_order = branches["combined_q2_q1"]
    permuted = branches["lineage_permuted"]
    diversion = branches["write_diversion"]
    clamp = branches["active_history_clamp"]
    state_only = branches["state_only_separation"]
    alternate = branches["alternate_responder"]
    checks.add("cross.order_equal_marginals", sorted(_token_amounts_from_branch(canonical)) == sorted(_token_amounts_from_branch(reversed_order)), _token_amounts_from_branch(reversed_order), _token_amounts_from_branch(canonical))
    checks.add("cross.order_equal_P", _close(canonical["coherences"]["P"], reversed_order["coherences"]["P"], freeze), reversed_order["coherences"]["P"], canonical["coherences"]["P"])
    checks.add("cross.order_history_differs", canonical["tokens"] != reversed_order["tokens"], reversed_order["tokens"], "different from canonical ordered H_P")
    checks.add("cross.order_response_differs", canonical["response"]["scheduled"] is True and reversed_order["response"]["scheduled"] is False, [canonical["response"]["scheduled"], reversed_order["response"]["scheduled"]], [True, False])
    checks.add("cross.lineage_causal_invariance", _causal_signature(permuted) == _causal_signature(canonical), _causal_signature(permuted), _causal_signature(canonical))
    checks.add("cross.lineage_audit_changed", permuted["source_lineages"] != canonical["source_lineages"], permuted["source_lineages"], "different from canonical lineage assignment")
    checks.add("cross.diversion_preserves_source_debits", [diversion["coherences"]["S1"], diversion["coherences"]["S2"]] == [canonical["coherences"]["S1"], canonical["coherences"]["S2"]], [diversion["coherences"]["S1"], diversion["coherences"]["S2"]], [canonical["coherences"]["S1"], canonical["coherences"]["S2"]])
    checks.add("cross.clamp_preserves_P", _close(clamp["coherences"]["P"], canonical["coherences"]["P"], freeze), clamp["coherences"]["P"], canonical["coherences"]["P"])
    checks.add("cross.clamp_changes_history_response", clamp["tokens"] == [] and clamp["response"]["scheduled"] is False and canonical["response"]["scheduled"] is True, {"tokens": clamp["tokens"], "scheduled": clamp["response"]["scheduled"]}, {"tokens": [], "scheduled": False})
    checks.add("cross.state_only_changes_P", not _close(state_only["coherences"]["P"], canonical["coherences"]["P"], freeze), state_only["coherences"]["P"], f"different from {canonical['coherences']['P']}")
    checks.add("cross.state_only_preserves_history_response", state_only["tokens"] == canonical["tokens"] and state_only["response"]["scheduled"] == canonical["response"]["scheduled"], {"tokens": state_only["tokens"], "scheduled": state_only["response"]["scheduled"]}, {"tokens": canonical["tokens"], "scheduled": canonical["response"]["scheduled"]})
    checks.add("cross.alternate_same_common_access", alternate["feedback"]["front_node_ids"] == canonical["feedback"]["front_node_ids"] and alternate["feedback"]["rear_node_ids"] == canonical["feedback"]["rear_node_ids"], {"front": alternate["feedback"]["front_node_ids"], "rear": alternate["feedback"]["rear_node_ids"]}, {"front": canonical["feedback"]["front_node_ids"], "rear": canonical["feedback"]["rear_node_ids"]})
    checks.add("cross.alternate_same_relation", _causal_signature(alternate) == _causal_signature(canonical), _causal_signature(alternate), _causal_signature(canonical))

    graph_after = _graph_guard()
    checks.add("guard.graph_revision_unchanged", graph_after["revision"] == runtime_receipt["graph_before"]["revision"], graph_after["revision"], runtime_receipt["graph_before"]["revision"])
    checks.add("guard.graph_clean_after", graph_after["status_porcelain"] == "", graph_after["status_porcelain"], "")
    for path, before_digest in runtime_receipt["graph_source_digests"].items():
        checks.add(f"guard.source_unchanged:{path}", _sha256(GRAPH_ROOT / path) == before_digest, _sha256(GRAPH_ROOT / path), before_digest)
    runtime_receipt["graph_after"] = graph_after

    return {
        "artifact_id": "P2-I2-I03B-HISTORY-CARRIED-RUNTIME-CONFORMANCE",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03B",
        "pool_dependence_mode": "history_carried",
        "realization_class": "minimally_producer_assisted",
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
        "producer_boundary": {
            "rcae_component": "RCAEActiveHistoryAdapterV1",
            "rcae_computes_success": False,
            "rcae_schedules_later_response": False,
            "native_feedback_producer_owns_later_transition": True,
        },
        "disposition": "history_carried_minimally_producer_assisted_runtime_conformant_pending_owner_review",
        "next_iteration_authorized": False,
    }


def _token_amounts_from_branch(branch: Mapping[str, Any]) -> list[float]:
    return [float(token["contact_amount"]) for token in branch["tokens"]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-freeze-only", action="store_true")
    args = parser.parse_args()
    freeze_path = args.freeze.resolve()
    freeze = _load_json(freeze_path)
    receipt = _validate_freeze(freeze, freeze_path)
    if args.validate_freeze_only:
        print(
            json.dumps(
                {
                    "status": "freeze_valid",
                    "runtime_operation_performed": False,
                    "runtime_receipt": receipt,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    _require(args.output is not None, "--output required for runtime conformance")
    record = _run_conformance(freeze, receipt)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical_json_bytes(record))
    print(
        json.dumps(
            {
                "status": record["status"],
                "assertion_summary": record["assertion_summary"],
                "output": str(output),
                "sha256": _sha256(output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
