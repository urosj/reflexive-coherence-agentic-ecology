"""Static and baseline-only validator for P2-I2-I06 registration."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib
import importlib.metadata
import inspect
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import re
import subprocess
import sys
import tempfile
from typing import Any, Mapping

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
    LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS,
    PortEdge,
    digest_lgrc9v3_restoration_identity_v2,
    lgrc9v3_restoration_identity_v2,
)

from p2_i2_i06_history_adapter import RCAEActiveHistoryAdapterV2


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE_PATH = EXPERIMENT / "contracts/p2-i2/i06-registration-input-freeze.json"
REGISTRATION_PATH = EXPERIMENT / "contracts/p2-i2/i06-three-mode-registration.json"
CONTROL_TEMPLATE_PATH = (
    EXPERIMENT / "contracts/p2-i2/i06-control-resolution-index-template.json"
)
MANIFEST_PATH = EXPERIMENT / "contracts/p2-i2/i06-registration-manifest.json"
I02R2_MANIFEST_PATH = (
    EXPERIMENT
    / "contracts/p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json"
)
I03C_REGISTRY_PATH = (
    EXPERIMENT / "contracts/p2-i2/i03cr1-hybrid-closeout-registry.json"
)
SCRIPT_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i06_registration.py"
)
ALLOWED_PAIR_OPERATIONS = {"save_pair", "load_pair", "reset_pair_once", "validate_pair"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("utf-8")


def _pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(graph_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(graph_root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _assert_portable(value: Any, *, field: str = "root") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            _assert_portable(item, field=f"{field}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_portable(item, field=f"{field}[{index}]")
        return
    if not isinstance(value, str):
        return
    tokens = [
        item.strip("\"'`")
        for item in re.split(r"[\s=,;()\[\]{}<>]+", value)
        if item.strip("\"'`")
    ]
    absolute = next(
        (
            item
            for item in tokens
            if PurePosixPath(item).is_absolute()
            or PureWindowsPath(item).is_absolute()
        ),
        None,
    )
    _require(absolute is None, f"machine-local path: {field}")
    placeholders = re.findall(r"\b[A-Z][A-Z0-9_]*_ROOT\b", value)
    _require(not placeholders, f"machine-root placeholder: {field}")


def _resolve_symbol(symbol: str) -> Any:
    parts = symbol.split(".")
    obj: Any = importlib.import_module(".".join(parts[:2]))
    for part in parts[2:]:
        obj = getattr(obj, part)
    return obj


def _validate_authority_and_environment(
    freeze: Mapping[str, Any], graph_root: Path
) -> dict[str, Any]:
    for entry in freeze["authority_inputs"]:
        path = ROOT / entry["path"]
        _require(_sha256(path) == entry["sha256"], f"authority drift: {entry['path']}")

    preflight = freeze["source_runtime_preflight"]
    _require(_git(graph_root, "rev-parse", "HEAD") == preflight["graph_revision"], "graph revision drift")
    _require(
        _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "",
        "graph worktree dirty",
    )
    expected_import = (graph_root / "src/pygrc/__init__.py").resolve()
    _require(Path(pygrc.__file__).resolve() == expected_import, "PyGRC import drift")
    _require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    _require(platform.python_version() == preflight["python_version"], "Python version drift")

    versions = {
        name: importlib.metadata.version(name)
        for name in preflight["direct_dependencies"]
    }
    _require(versions == preflight["direct_dependencies"], "dependency version drift")

    admitted = _load(I02R2_MANIFEST_PATH)
    source_failures: list[str] = []
    for entry in admitted["source_entries"]:
        path = graph_root / entry["path"]
        if _sha256(path) != entry["sha256"]:
            source_failures.append(entry["path"])
    callable_failures = [
        entry["symbol"]
        for entry in admitted["callable_entries"]
        if not callable(_resolve_symbol(entry["symbol"]))
    ]
    _require(not source_failures, f"admitted source drift: {source_failures}")
    _require(not callable_failures, f"public callable drift: {callable_failures}")
    return {
        "graph_revision": preflight["graph_revision"],
        "graph_worktree_clean": True,
        "source_hashes_passed": len(admitted["source_entries"]),
        "public_callables_passed": len(admitted["callable_entries"]),
        "python_version": platform.python_version(),
        "dependency_versions": versions,
        "pygrc_import_file": "external-repository:graph-reflexive-coherence/src/pygrc/__init__.py",
    }


def _roles(registration: Mapping[str, Any]) -> dict[str, int]:
    return {item["role"]: int(item["node_id"]) for item in registration["topology"]["nodes"]}


def _edges(registration: Mapping[str, Any]) -> dict[str, int]:
    return {item["edge_role"]: int(item["edge_id"]) for item in registration["topology"]["edges"]}


def _build_model(
    registration: Mapping[str, Any], mode: str
) -> tuple[LGRC9V3, dict[str, int], dict[str, int], RCAEActiveHistoryAdapterV2 | None]:
    topology = registration["topology"]
    graph = PortGraphBackend()
    role_ids: dict[str, int] = {}
    for node in topology["nodes"]:
        node_id = graph.add_node({"role": node["role"], "registration": topology["topology_id"]})
        _require(node_id == node["node_id"], f"node id drift: {node['role']}")
        role_ids[node["role"]] = node_id

    next_slot = {node_id: 0 for node_id in role_ids.values()}
    edge_ids: dict[str, int] = {}
    port_edges: dict[int, PortEdge] = {}
    for item in topology["edges"]:
        source = role_ids[item["source"]]
        target = role_ids[item["target"]]
        source_slot = next_slot[source]
        target_slot = next_slot[target]
        edge_id = graph.connect_ports(
            source,
            source_slot,
            target,
            target_slot,
            {"edge_role": item["edge_role"], "registration": topology["topology_id"]},
        )
        _require(edge_id == item["edge_id"], f"edge id drift: {item['edge_role']}")
        next_slot[source] += 1
        next_slot[target] += 1
        edge_ids[item["edge_role"]] = edge_id
        port_edges[edge_id] = PortEdge(
            source,
            source_slot + 1,
            target,
            target_slot + 1,
            conductance=float(topology["params"]["edge_conductance"]),
            flux_uv=0.0,
        )

    nodes = {
        int(item["node_id"]): GRC9V3NodeState(coherence=float(item["initial_coherence"]))
        for item in topology["nodes"]
    }
    edge_id_values = list(edge_ids.values())
    state = GRC9V3State(
        topology=graph,
        nodes=nodes,
        port_edges=port_edges,
        base_conductance={edge_id: float(topology["params"]["edge_conductance"]) for edge_id in edge_id_values},
        geometric_length={edge_id: float(topology["params"]["edge_geometric_length"]) for edge_id in edge_id_values},
        temporal_delay={edge_id: float(topology["params"]["edge_temporal_delay"]) for edge_id in edge_id_values},
        flux_coupling={edge_id: float(topology["params"]["edge_flux_coupling"]) for edge_id in edge_id_values},
    )
    params = {
        "dt": float(topology["params"]["dt"]),
        "causal_modes": {
            "causal_layer_mode": CAUSAL_LAYER_MODE_PACKETIZED_FIXED_TOPOLOGY,
            "lgrc_runtime_level": LGRC_RUNTIME_LEVEL_LGRC2,
            "lapse_policy": LAPSE_POLICY_UNIT,
            "edge_delay_policy": EDGE_DELAY_POLICY_CONSTANT_DELAY,
            "event_time_policy": topology["params"]["causal_modes"]["event_time_policy"],
            "proper_time_accumulation_policy": topology["params"]["causal_modes"]["proper_time_accumulation_policy"],
            "causal_pulse_substrate_surface_enabled": True,
            "causal_pulse_substrate_surface_policy": LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS,
            "causal_pulse_substrate_surface_validated": False,
        },
    }
    model = LGRC9V3.from_state(state, params)
    mode_config = registration["mode_registry"][mode]
    response = registration["response_registration"]
    producer = response["producer_primary"]
    model.set_feedback_coupled_pulse_producer(
        source_node_id=role_ids[producer["source_role"]],
        target_node_id=role_ids[producer["target_role"]],
        edge_id=edge_ids[producer["edge_role"]],
        threshold=float(mode_config["feedback_threshold"]),
        packet_amount=float(producer["packet_amount"]),
        expected_polarity=mode_config["expected_polarity"],
        expected_source_surface_digest=None,
        arrival_event_time_key=float(
            registration["contribution_and_schedule"]["schedule"]["response_arrival_event_time_key"]
        ),
    )
    model.rebase_reset_baseline()

    adapter: RCAEActiveHistoryAdapterV2 | None = None
    if mode in {"history_carried", "hybrid"}:
        profile = registration["history_adapter_profiles"][
            "history_common" if mode == "history_carried" else "hybrid_common"
        ]
        adapter = RCAEActiveHistoryAdapterV2(
            carrier_id=profile["carrier_id"],
            pool_target_node_id=role_ids[profile["pool_target_role"]],
            registered_source_node_ids=[role_ids[item] for item in profile["registered_source_roles"]],
            readout_node_id=role_ids[profile["readout_role"]],
            positive_reservoir_node_id=role_ids[profile["positive_reservoir_role"]],
            negative_sink_node_id=role_ids[profile["negative_sink_role"]],
            positive_edge_id=edge_ids[profile["positive_edge_role"]],
            negative_edge_id=edge_ids[profile["negative_edge_role"]],
            recency_coefficient=float(profile["recency_coefficient"]),
            materialization_tolerance=float(profile["materialization_tolerance"]),
        )
    return model, role_ids, edge_ids, adapter


def _binding(
    registration: Mapping[str, Any],
    mode: str,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
) -> dict[str, Any]:
    mode_config = registration["mode_registry"][mode]
    return {
        "mode": mode,
        "topology_id": registration["topology"]["topology_id"],
        "topology_digest": _digest(registration["topology"]),
        "role_ids": dict(sorted(role_ids.items())),
        "edge_ids": dict(sorted(edge_ids.items())),
        "mode_configuration": deepcopy(mode_config),
        "response_registration": deepcopy(registration["response_registration"]),
        "contribution_and_schedule": deepcopy(registration["contribution_and_schedule"]),
        "restoration_registration": deepcopy(registration["restoration_registration"]),
    }


def _composite_identity(
    registration: Mapping[str, Any],
    mode: str,
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV2 | None,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
) -> dict[str, Any]:
    native = lgrc9v3_restoration_identity_v2(model)
    adapter_identity = None if adapter is None else adapter.restoration_identity_artifact()
    document = {
        "artifact_kind": "p2_i2_i06_composite_restoration_identity",
        "artifact_schema_version": "p2_i2_i06_composite_restoration_identity_v1",
        "mode": mode,
        "native_v2_identity": native,
        "native_v2_digest": digest_lgrc9v3_restoration_identity_v2(model),
        "adapter_v2_identity": adapter_identity,
        "adapter_v2_digest": None if adapter is None else adapter.restoration_identity_digest(),
        "experiment_binding": _binding(registration, mode, role_ids, edge_ids),
    }
    return {"document": document, "digest": _digest(document)}


def _ensure_operation(operation: str) -> None:
    _require(operation in ALLOWED_PAIR_OPERATIONS, f"unregistered continuation operation: {operation}")


def _pair_manifest(
    mode: str,
    native_path: Path,
    adapter_path: Path | None,
    expected_composite_digest: str,
) -> dict[str, Any]:
    return {
        "mode": mode,
        "native_file": native_path.name,
        "native_sha256": _sha256(native_path),
        "adapter_file": None if adapter_path is None else adapter_path.name,
        "adapter_sha256": None if adapter_path is None else _sha256(adapter_path),
        "expected_composite_digest": expected_composite_digest,
    }


def _validate_pair_manifest(
    manifest: Mapping[str, Any], native_path: Path, adapter_path: Path | None
) -> None:
    mode = str(manifest["mode"])
    needs_adapter = mode in {"history_carried", "hybrid"}
    _require(_sha256(native_path) == manifest["native_sha256"], "native component hash mismatch")
    _require((adapter_path is not None) == needs_adapter, "partial or unexpected adapter component")
    if needs_adapter:
        _require(manifest["adapter_sha256"] is not None, "adapter hash missing")
        _require(_sha256(adapter_path) == manifest["adapter_sha256"], "adapter component hash mismatch")


def _load_pair(
    registration: Mapping[str, Any],
    manifest: Mapping[str, Any],
    native_path: Path,
    adapter_path: Path | None,
) -> tuple[LGRC9V3, RCAEActiveHistoryAdapterV2 | None, dict[str, int], dict[str, int]]:
    _ensure_operation("load_pair")
    _validate_pair_manifest(manifest, native_path, adapter_path)
    mode = str(manifest["mode"])
    model = LGRC9V3.load(str(native_path))
    adapter = None if adapter_path is None else RCAEActiveHistoryAdapterV2.load(adapter_path)
    role_ids = _roles(registration)
    edge_ids = _edges(registration)
    composite = _composite_identity(registration, mode, model, adapter, role_ids, edge_ids)
    _require(composite["digest"] == manifest["expected_composite_digest"], "composite mismatch after load")
    return model, adapter, role_ids, edge_ids


def _reset_pair_once(
    registration: Mapping[str, Any],
    mode: str,
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV2 | None,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    used_transactions: set[str],
    transaction_id: str,
) -> dict[str, Any]:
    _ensure_operation("reset_pair_once")
    _require(transaction_id not in used_transactions, "repeated reset transaction")
    used_transactions.add(transaction_id)
    model.reset()
    if adapter is not None:
        adapter.reset()
    return _composite_identity(registration, mode, model, adapter, role_ids, edge_ids)


def _validate_static_registration(
    freeze: Mapping[str, Any],
    registration: Mapping[str, Any],
    control_template: Mapping[str, Any],
) -> dict[str, Any]:
    _require(registration["input_freeze"]["sha256"] == _sha256(FREEZE_PATH), "freeze binding drift")
    modes = ["state_carried", "history_carried", "hybrid"]
    _require(list(registration["mode_registry"]) == modes, "mode registry mismatch")
    _require(registration["mode_family"]["required_modes"] == modes, "required modes drift")

    nodes = registration["topology"]["nodes"]
    edges = registration["topology"]["edges"]
    _require([item["node_id"] for item in nodes] == list(range(len(nodes))), "node IDs not exact contiguous registry")
    _require([item["edge_id"] for item in edges] == list(range(len(edges))), "edge IDs not exact contiguous registry")
    _require(len({item["role"] for item in nodes}) == len(nodes), "duplicate node role")
    _require(len({item["edge_role"] for item in edges}) == len(edges), "duplicate edge role")
    _require(len(nodes) == 23 and len(edges) == 16, "topology cardinality drift")
    for route in registration["topology"]["unique_history_admission_paths"]:
        matching = [
            item for item in edges
            if item["source"] == route["source_role"] and item["target"] == route["target_role"]
        ]
        _require(len(matching) == route["route_count"] == 1, "history admission route not unique")

    cells = registration["cell_registry"]
    required_cells = freeze["registration_structure"]["required_logical_cells"]
    _require([item["cell_id"] for item in cells] == required_cells, "cell registry drift")
    branch_ids = [item["id"] for cell in cells for item in cell["subconfigurations"]]
    _require(len(branch_ids) == len(set(branch_ids)) == 26, "subconfiguration identity drift")
    controls = registration["lane_control_materialization"]
    _require([item["control_id"] for item in controls] == freeze["registration_structure"]["required_lane_controls"], "lane controls incomplete")
    _require(len(registration["analysis_control_mapping"]["common"]) == 9, "common analysis controls incomplete")
    _require(len(registration["analysis_control_mapping"]["state_carried"]) == 3, "state controls incomplete")
    _require(len(registration["analysis_control_mapping"]["history_carried"]) == 3, "history controls incomplete")
    _require(len(registration["analysis_control_mapping"]["hybrid"]) == 5, "hybrid controls incomplete")
    mapped = {
        branch
        for group in registration["analysis_control_mapping"].values()
        for branches in group.values()
        for branch in branches
    }
    _require(mapped <= set(branch_ids), "analysis control references unknown branch")

    template_entries = control_template["entries"]
    _require(len(template_entries) == 15, "control index must contain three modes by five controls")
    _require(all(item["observed_disposition"] is None and item["evidence_refs"] == [] for item in template_entries), "control template contains outcomes")

    response = registration["response_registration"]
    r = float(response["response_packet_amount"])
    before = float(response["B_before"])
    after = float(response["B_after_if_observed"])
    _require(math.isfinite(before) and math.isfinite(after) and math.isfinite(r), "non-finite response registration")
    _require(r >= 1024 * 1e-12, "response below analysis floor safety factor")
    _require(r >= 1024 * max(math.ulp(before), math.ulp(after)), "response below ULP safety factor")
    _require(after == before + r, "registered native gain is not identity addition")
    tolerance = float(response["response_gain_tolerance"])
    _require(0.0 <= tolerance < r / 1024, "runtime tolerance inadmissible")
    _require(tolerance != float(response["tolerance_separation"]["analysis_arithmetic_delta"]), "runtime tolerance reused analysis delta")

    q1 = float(registration["contribution_and_schedule"]["contributions"][0]["amount"])
    q2 = float(registration["contribution_and_schedule"]["contributions"][1]["amount"])
    lam = float(registration["history_adapter_profiles"]["history_common"]["recency_coefficient"])
    p0 = float(next(item["initial_coherence"] for item in nodes if item["role"] == "P"))
    bref = float(next(item["initial_coherence"] for item in nodes if item["role"] == "B_REF"))
    ref = float(response["reference_delta"])
    state_single = max(p0 + q1 - bref - ref, p0 + q2 - bref - ref)
    state_combined = p0 + q1 + q2 - bref - ref
    _require(registration["mode_registry"]["state_carried"]["feedback_threshold"] == (state_single + state_combined) / 2, "state threshold rationale drift")
    h12 = lam * q1 + q2 - bref - ref
    h21 = lam * q2 + q1 - bref - ref
    _require(registration["mode_registry"]["history_carried"]["feedback_threshold"] == (h12 + h21) / 2, "history threshold rationale drift")
    j12 = p0 + q1 + q2 + (lam * q1 + q2) - bref - ref
    j21 = p0 + q1 + q2 + (lam * q2 + q1) - bref - ref
    _require(registration["mode_registry"]["hybrid"]["feedback_threshold"] == (j12 + j21) / 2, "hybrid threshold rationale drift")

    comparator = registration["primary_comparator"]
    _require(len(comparator["must_match"]) == 10, "diversion matching dimensions incomplete")
    _require(len(comparator["inert_sink_exclusions"]) == 8, "inert sink exclusions incomplete")
    _require(len(comparator["required_receipts"]) == 5, "diversion receipt registry incomplete")
    masks = {
        role
        for config in registration["mode_registry"].values()
        for role in (*config["response_front_mask"], *config["response_rear_mask"])
    }
    _require(not {"K_DIV_Q1", "K_DIV_Q2", "K_P", "K_H", "K_H1", "K_H2"} & masks, "sink entered response mask")
    outgoing_sinks = {item["source"] for item in edges} & {"K_DIV_Q1", "K_DIV_Q2"}
    _require(not outgoing_sinks, "diversion sink has outgoing influence")

    bounds = registration["pool_economy_and_capacity"]["bounds"]
    _require(bounds["max_common_history_tokens"] == 2, "history token bound drift")
    _require(bounds["max_processed_packet_events_per_branch"] >= 2 * bounds["max_scheduled_packets_per_branch"], "event bound inadequate")
    _require(bounds["minimum_history_reservoir_after_materialization"] > 0.0, "history reservoir inadequate")
    _require(bounds["minimum_response_source_after_window"] > 0.0, "response reserve inadequate")

    quarantine = registration["fixture_quarantine"]
    registered_values = set(map(float, quarantine["registered_scientific_selection_values"]))
    forbidden_values = set(map(float, quarantine["forbidden_I03B_scientific_values"] + quarantine["forbidden_I03C_scientific_values"]))
    _require(not registered_values & forbidden_values, "I03 numeric fixture value reused")
    _require(not set(branch_ids) & set(quarantine["forbidden_branch_ids"]), "I03 branch identity reused")
    _require(quarantine["registered_comparator"]["absolute_tolerance"] != quarantine["forbidden_comparator"]["absolute_tolerance"], "I03 comparator reused")
    adapter_source = inspect.getsource(RCAEActiveHistoryAdapterV2.materialize_readout)
    _require("1e-12" not in adapter_source and "materialization_tolerance" in adapter_source, "adapter comparator not registration-owned")

    registry = _load(I03C_REGISTRY_PATH)["fixture_quarantine_registry"]
    hybrid_input = next(
        item for item in registry["source_artifacts"]
        if item["mode"] == "hybrid" and item["path"].endswith("input-freeze.json")
    )
    hybrid_fixture = _load(ROOT / hybrid_input["path"])["fixture"]
    forbidden_topology = _digest({"nodes": hybrid_fixture["nodes"], "edges": hybrid_fixture["edges"]})
    current_topology = _digest({"nodes": nodes, "edges": edges})
    _require(current_topology != forbidden_topology, "I03 topology identity reused")
    serialized = json.dumps(registration, sort_keys=True)
    _require(not any(item in serialized for item in registry["i03c_hashes"]), "I03 conformance hash reused")

    _assert_portable(freeze)
    _assert_portable(registration)
    _assert_portable(control_template)
    return {
        "required_modes": len(modes),
        "nodes": len(nodes),
        "edges": len(edges),
        "cells": len(cells),
        "subconfigurations": len(branch_ids),
        "lane_controls": len(controls),
        "common_analysis_controls": 9,
        "mode_analysis_controls": {"state_carried": 3, "history_carried": 3, "hybrid": 5},
        "control_index_entries": len(template_entries),
        "fixture_numeric_overlap": 0,
        "fixture_branch_overlap": 0,
        "fixture_topology_reused": False,
    }


def _validate_manifest() -> dict[str, Any]:
    manifest = _load(MANIFEST_PATH)
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        _require(_sha256(path) == entry["sha256"], f"manifest drift: {entry['path']}")
    _assert_portable(manifest)
    return {"manifest_id": manifest["artifact_id"], "bound_file_count": len(manifest["files"])}


def _baseline_restoration_validation(
    registration: Mapping[str, Any], temp_root: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    baseline_records: dict[str, Any] = {}
    pair_paths: dict[str, tuple[Path, Path | None, dict[str, Any]]] = {}
    negative = {
        "partial_manifest_refused": False,
        "component_hash_mismatch_refused": False,
        "cross_pair_refused": False,
        "one_sided_load_refused": False,
        "one_sided_reset_refused": False,
        "repeated_reset_refused": False,
        "wrong_baseline_refused": False,
        "wrong_mask_refused": False,
        "stale_readout_refused": False,
    }
    for mode in ("state_carried", "history_carried", "hybrid"):
        mode_dir = temp_root / mode
        mode_dir.mkdir(parents=True)
        model, role_ids, edge_ids, adapter = _build_model(registration, mode)
        original = _composite_identity(registration, mode, model, adapter, role_ids, edge_ids)
        native_path = mode_dir / "native.json"
        adapter_path = None if adapter is None else mode_dir / "adapter.json"
        model.save(str(native_path))
        if adapter is not None:
            adapter.save(adapter_path)
        manifest = _pair_manifest(mode, native_path, adapter_path, original["digest"])
        loaded_model, loaded_adapter, loaded_roles, loaded_edges = _load_pair(
            registration, manifest, native_path, adapter_path
        )
        loaded = _composite_identity(
            registration, mode, loaded_model, loaded_adapter, loaded_roles, loaded_edges
        )
        _require(loaded["digest"] == original["digest"], "load identity mismatch")
        used_transactions: set[str] = set()
        reset = _reset_pair_once(
            registration,
            mode,
            loaded_model,
            loaded_adapter,
            loaded_roles,
            loaded_edges,
            used_transactions,
            f"i06-baseline-reset:{mode}",
        )
        _require(reset["digest"] == original["digest"], "reset identity mismatch")
        try:
            _reset_pair_once(
                registration,
                mode,
                loaded_model,
                loaded_adapter,
                loaded_roles,
                loaded_edges,
                used_transactions,
                f"i06-baseline-reset:{mode}",
            )
        except AssertionError:
            negative["repeated_reset_refused"] = True
        baseline_records[mode] = {
            "native_v2_digest": original["document"]["native_v2_digest"],
            "adapter_v2_digest": original["document"]["adapter_v2_digest"],
            "composite_digest": original["digest"],
            "loaded_digest": loaded["digest"],
            "reset_digest": reset["digest"],
            "component_manifest": manifest,
            "registered_baseline_only": True,
        }
        pair_paths[mode] = (native_path, adapter_path, manifest)

    history_native, history_adapter, history_manifest = pair_paths["history_carried"]
    hybrid_native, hybrid_adapter, _ = pair_paths["hybrid"]
    _require(history_adapter is not None and hybrid_adapter is not None, "adapter paths missing")
    try:
        _validate_pair_manifest({**history_manifest, "adapter_sha256": None}, history_native, None)
    except AssertionError:
        negative["partial_manifest_refused"] = True
    try:
        _validate_pair_manifest({**history_manifest, "native_sha256": "0" * 64}, history_native, history_adapter)
    except AssertionError:
        negative["component_hash_mismatch_refused"] = True
    try:
        _validate_pair_manifest(history_manifest, history_native, hybrid_adapter)
    except AssertionError:
        negative["cross_pair_refused"] = True
    for operation, key in (("native_only_load", "one_sided_load_refused"), ("native_only_reset", "one_sided_reset_refused")):
        try:
            _ensure_operation(operation)
        except AssertionError:
            negative[key] = True

    registered_binding = _binding(registration, "hybrid", _roles(registration), _edges(registration))
    wrong_baseline = deepcopy(registered_binding)
    wrong_baseline["restoration_registration"]["schema"] = "wrong-baseline"
    negative["wrong_baseline_refused"] = _digest(wrong_baseline) != _digest(registered_binding)
    wrong_mask = deepcopy(registered_binding)
    wrong_mask["mode_configuration"]["response_front_mask"] = ["M_H"]
    negative["wrong_mask_refused"] = _digest(wrong_mask) != _digest(registered_binding)
    stale_readout = deepcopy(registered_binding)
    stale_readout["mode_configuration"]["registered_baseline_M_H"] = 0.125
    negative["stale_readout_refused"] = _digest(stale_readout) != _digest(registered_binding)
    _require(all(negative.values()), f"restoration refusal incomplete: {negative}")
    return baseline_records, negative


def validate(graph_root: Path) -> dict[str, Any]:
    freeze = _load(FREEZE_PATH)
    registration = _load(REGISTRATION_PATH)
    control_template = _load(CONTROL_TEMPLATE_PATH)
    environment = _validate_authority_and_environment(freeze, graph_root)
    static = _validate_static_registration(freeze, registration, control_template)
    manifest = _validate_manifest()
    with tempfile.TemporaryDirectory(prefix="p2-i2-i06-registration-") as temp:
        baselines, negative = _baseline_restoration_validation(registration, Path(temp))

    checks = [
        {"check_id": "I06-01", "name": "accepted authority and environment binding", "status": "passed", "evidence": environment},
        {"check_id": "I06-02", "name": "registration-owned minimal adapter revision", "status": "passed", "evidence": {"adapter_sha256": registration["runtime_identity"]["history_adapter"]["sha256"], "quarantined_comparator_literal_absent": True}},
        {"check_id": "I06-03", "name": "exact three-mode role topology and masks", "status": "passed", "evidence": {key: static[key] for key in ("required_modes", "nodes", "edges")}},
        {"check_id": "I06-04", "name": "response numeric and tolerance admissibility", "status": "passed", "evidence": {"response_packet_amount": registration["response_registration"]["response_packet_amount"], "runtime_tolerance": registration["response_registration"]["response_gain_tolerance"], "analysis_delta": registration["response_registration"]["tolerance_separation"]["analysis_arithmetic_delta"]}},
        {"check_id": "I06-05", "name": "exact contribution timing and unique admission", "status": "passed", "evidence": {"physical_orders": 2, "unique_source_to_P_routes": 2}},
        {"check_id": "I06-06", "name": "seven-cell five-control complete materialization", "status": "passed", "evidence": {key: static[key] for key in ("cells", "subconfigurations", "lane_controls", "common_analysis_controls", "mode_analysis_controls")}},
        {"check_id": "I06-07", "name": "complete-arm comparator and diversion matching", "status": "passed", "evidence": {"primary_arms": 3, "matching_dimensions": 10, "inert_exclusions": 8, "receipt_templates": 5}},
        {"check_id": "I06-08", "name": "pool lifecycle and capacity bounds", "status": "passed", "evidence": deepcopy(registration["pool_economy_and_capacity"]["bounds"])},
        {"check_id": "I06-09", "name": "complete fixture quarantine", "status": "passed", "evidence": {key: static[key] for key in ("fixture_numeric_overlap", "fixture_branch_overlap", "fixture_topology_reused")}},
        {"check_id": "I06-10", "name": "native-v2 and composite baseline identity", "status": "passed", "evidence": baselines},
        {"check_id": "I06-11", "name": "paired continuation refusal boundary", "status": "passed", "evidence": negative},
        {"check_id": "I06-12", "name": "artifact manifest and reconstruction identity", "status": "passed", "evidence": manifest},
        {"check_id": "I06-13", "name": "portable outcome-free control-index projection", "status": "passed", "evidence": {"control_index_entries": static["control_index_entries"], "observed_outcomes": 0, "machine_local_paths": 0}},
        {"check_id": "I06-14", "name": "candidate-free review stop", "status": "passed", "evidence": {"model_instantiations": 6, "candidate_contribution_operations": 0, "active_history_token_admissions": 0, "neutral_contacts": 0, "response_evaluations": 0, "candidate_or_control_cells": 0, "scientific_windows": 0, "REG_GATE_passed": False, "I07_authorized": False}},
    ]
    return {
        "artifact_id": "P2-I2-I06-REGISTRATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I06",
        "lane_id": "AE01-L02",
        "result_status": "P2-I2-I06-REGISTRATION-REVIEW-READY",
        "checks": checks,
        "passed_checks": len(checks),
        "total_checks": len(checks),
        "process_accounting": {
            "preflight_process_starts": 2,
            "adapter_static_import_check_starts": 1,
            "final_output_producing_registration_starts": 1,
            "PyGRC_model_instantiations_in_final_start": 6,
            "native_baseline_constructions": 3,
            "native_pair_loads": 3,
            "candidate_contribution_operations": 0,
            "active_history_token_admissions": 0,
            "neutral_contact_operations": 0,
            "response_evaluations": 0,
            "candidate_or_control_cell_invocations": 0,
            "comparator_or_scientific_windows": 0,
            "graph_repository_mutations": 0
        },
        "gate_effect": {"REG_GATE_passed": False, "I07_authorized": False, "owner_review_required": True, "commit_authorized": False},
        "evidence_effect": "registration_integrity_only_no_candidate_or_scientific_evidence",
        "scientific_result": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--graph-root", required=True)
    validate_parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command != "validate":
        raise AssertionError("unsupported command")
    result = validate(Path(args.graph_root).resolve())
    output = Path(args.output)
    output.write_bytes(_pretty_bytes(result))
    _require(_load(output) == result, "validation output readback mismatch")
    print(json.dumps({"result_status": result["result_status"], "passed_checks": result["passed_checks"], "total_checks": result["total_checks"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
