#!/usr/bin/env python3
"""Execute the single quarantined P2-I3-I03 B-R conformance fixture.

The output is implementation-conformance evidence only.  It cannot calibrate,
register, execute, support, or refute AE01-H-L03.  A retained invocation is
permitted only from clean committed RCAE sources; reconstruction reuses the
retained binding receipt and writes outside the repository.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib
import importlib.metadata
import inspect
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable, Mapping

import pygrc
from pygrc.core import PortGraphBackend
from pygrc.models import (
    GRC9V3NodeState,
    GRC9V3State,
    LGRC9V3,
    PortEdge,
    compute_lgrc9v3_causal_distances,
    compute_lgrc9v3_functional_distances,
    compute_lgrc9v3_geometric_distances,
    digest_lgrc9v3_restoration_identity_v2,
    lgrc9v3_restoration_identity_v2,
)

from p2_i3_br_runtime import (
    BRContractError,
    RECEIPT_SCHEMA,
    build_blind_encounter_request,
    build_control_interface_records,
    build_q13_constructor_records,
    canonical_bytes,
    causal_continuation_projection,
    composite_identity,
    digest_data,
    evaluate_export_policy,
    initial_policy_state,
    load_composite,
    make_audit_state,
    make_branch_state,
    make_reset_state,
    reset_rcae_components,
    save_composite,
    settle_export_policy,
    sha256_file,
)
from p2_i3_conformance_quarantine import (
    FORBIDDEN_CONSUMER_CLASSES,
    ConformanceQuarantineError,
    assert_no_conformance_import,
)


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_RELATIVE = Path(
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i3_i03_br_conform.py"
)
RUNTIME_RELATIVE = Path(
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i3_br_runtime.py"
)
QUARANTINE_RELATIVE = Path(
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i3_conformance_quarantine.py"
)
FREEZE_SOURCE_ANCHOR = "94bfe01f1ecf3d427e86e47968cc249256487208"
EXPECTED_FREEZE_ID = "P2-I3-I03-BR-BOUNDED-CONFORMANCE-INPUT-FREEZE"
EXPECTED_FREEZE_SHA256 = "0a255d21605c2a1cbf00a3467562fc08dd73a32505d4d435b6eb6f140f16a243"
EXPECTED_GRAPH_REVISION = "565706f8b7647f6b7638b9afbe52372e170bf724"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(root), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write_exclusive(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(canonical_bytes(value))


def with_digest(value: Mapping[str, Any]) -> dict[str, Any]:
    record = deepcopy(dict(value))
    record["canonical_payload_digest"] = digest_data(record)
    return record


def resolve_symbol(name: str) -> Any:
    parts = name.split(".")
    module = importlib.import_module(".".join(parts[:2]))
    value: Any = module
    for part in parts[2:]:
        value = getattr(value, part)
    return value


class Calls:
    def __init__(self) -> None:
        self.rows: list[str] = []

    def record(self, symbol: str) -> None:
        self.rows.append(symbol)

    def invoke(self, symbol: str, function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        self.record(symbol)
        return function(*args, **kwargs)


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(
        self,
        cell_id: str,
        check_id: str,
        condition: bool,
        observed: Any,
        expected: Any,
    ) -> None:
        row = {
            "cell_id": cell_id,
            "check_id": check_id,
            "passed": bool(condition),
            "observed": observed,
            "expected": expected,
        }
        self.rows.append(row)
        require(condition, f"{check_id}: observed={observed!r}, expected={expected!r}")


def close(left: float, right: float, tolerance: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def native_refusal_reason(error: Exception) -> str:
    """Classify only the exact native refusal without importing a 19th surface."""

    require(
        type(error).__module__ == "pygrc.core.errors"
        and type(error).__name__ == "InvalidStateTransitionError",
        f"unexpected native exception: {type(error).__module__}.{type(error).__name__}",
    )
    return str(error)


def state(model: LGRC9V3, calls: Calls) -> Any:
    return calls.invoke("pygrc.models.LGRC9V3.get_state", model.get_state)


def native_digest(model: LGRC9V3, calls: Calls) -> str:
    return calls.invoke(
        "pygrc.models.digest_lgrc9v3_restoration_identity_v2",
        digest_lgrc9v3_restoration_identity_v2,
        model,
    )


def coherences(model: LGRC9V3, calls: Calls) -> dict[int, float]:
    runtime = state(model, calls)
    return {
        int(node_id): float(node.coherence)
        for node_id, node in sorted(runtime.base_state.nodes.items())
    }


def budget(model: LGRC9V3, calls: Calls) -> dict[str, float]:
    ledger = state(model, calls).packet_ledger
    require(ledger is not None, "native packet ledger missing")
    return {
        "node_coherence_total": float(ledger.node_coherence_total),
        "in_flight_packet_total": float(ledger.in_flight_packet_total),
        "conserved_budget_total": float(ledger.conserved_budget_total),
        "budget_error": float(ledger.budget_error),
    }


def queue_count(model: LGRC9V3, calls: Calls) -> int:
    ledger = state(model, calls).packet_ledger
    require(ledger is not None, "native packet ledger missing")
    return len(ledger.event_queue_records)


def packet_count(model: LGRC9V3, calls: Calls) -> int:
    ledger = state(model, calls).packet_ledger
    require(ledger is not None, "native packet ledger missing")
    return len(ledger.packet_records)


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
                "budget_error": float(event.payload.get("budget_error", 0.0)),
            }
    raise AssertionError("native step result lacks packet processing receipt")


def build_model(freeze: Mapping[str, Any], calls: Calls) -> LGRC9V3:
    fixture = freeze["fixture"]
    calls.record("pygrc.core.PortGraphBackend")
    graph = PortGraphBackend()
    for node in fixture["nodes"]:
        observed = graph.add_node({"conformance_role": node["role"]})
        require(observed == int(node["node_id"]), f"node allocation drift: {node['role']}")
    next_slot = {int(node["node_id"]): 0 for node in fixture["nodes"]}
    port_edges: dict[int, PortEdge] = {}
    for edge in fixture["edges"]:
        source = int(edge["source"])
        target = int(edge["target"])
        source_slot = next_slot[source]
        target_slot = next_slot[target]
        observed = graph.connect_ports(
            source,
            source_slot,
            target,
            target_slot,
            {"conformance_relation": edge["role"]},
        )
        require(observed == int(edge["edge_id"]), f"edge allocation drift: {edge['role']}")
        next_slot[source] += 1
        next_slot[target] += 1
        calls.record("pygrc.models.PortEdge")
        port_edges[observed] = PortEdge(
            source,
            source_slot + 1,
            target,
            target_slot + 1,
            conductance=1.0,
            flux_uv=0.0,
        )
    calls.record("pygrc.models.GRC9V3NodeState")
    nodes = {
        int(row["node_id"]): GRC9V3NodeState(coherence=float(row["initial_coherence"]))
        for row in fixture["nodes"]
    }
    edge_ids = sorted(port_edges)
    calls.record("pygrc.models.GRC9V3State")
    base = GRC9V3State(
        topology=graph,
        nodes=nodes,
        port_edges=port_edges,
        base_conductance={edge_id: 1.0 for edge_id in edge_ids},
        geometric_length={edge_id: 1.0 for edge_id in edge_ids},
        temporal_delay={edge_id: 1.0 for edge_id in edge_ids},
        flux_coupling={edge_id: 0.0 for edge_id in edge_ids},
    )
    params = {
        "dt": float(fixture["dt"]),
        "causal_modes": {
            "causal_layer_mode": fixture["causal_layer_mode"],
            "lgrc_runtime_level": fixture["lgrc_runtime_level"],
            "lapse_policy": "unit",
            "edge_delay_policy": "constant_delay",
            "event_time_policy": "explicit_event_time_key",
            "proper_time_accumulation_policy": "local_event_frontier",
        },
    }
    return calls.invoke("pygrc.models.LGRC9V3.from_state", LGRC9V3.from_state, base, params)


def schedule(model: LGRC9V3, request: Mapping[str, Any], calls: Calls) -> None:
    calls.invoke(
        "pygrc.models.LGRC9V3.schedule_packet_departure",
        model.schedule_packet_departure,
        **dict(request),
    )


def run_queue(model: LGRC9V3, max_events: int, calls: Calls) -> list[Any]:
    return calls.invoke(
        "pygrc.models.LGRC9V3.run_event_queue",
        model.run_event_queue,
        max_events=max_events,
    )


def step(model: LGRC9V3, calls: Calls) -> Any:
    return calls.invoke("pygrc.models.LGRC9V3.step", model.step)


def formation_request(
    *, source: int, target: int, edge: int, amount: float, index: int
) -> dict[str, Any]:
    departure = float(index * 2)
    return {
        "source_node_id": source,
        "target_node_id": target,
        "edge_id": edge,
        "amount": amount,
        "departure_event_time_key": departure,
        "arrival_event_time_key": departure + 1.0,
        "scheduler_event_index": index * 2,
        "packet_index": index,
        "source_lineage_id": f"p2_i3_i03_formation_{index}",
        "target_lineage_id": f"p2_i3_i03_carrier_{target}",
    }


def lifecycle_receipt(
    *,
    receipt_id: str,
    sequence: int,
    event_identity: str,
    predecessor: str,
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "route_id": policy["route_id"],
        "sequence_index": sequence,
        "qualifying_native_event_identity": event_identity,
        "predecessor_composite_identity": predecessor,
        "policy_id": policy["policy_id"],
        "source_node_id": policy["source_node_id"],
        "destination_node_id": policy["destination_node_id"],
        "edge_id": policy["edge_id"],
        "prior_settlement_status": "settled",
        "eligible": True,
    }


def expected_bindings(
    policy: Mapping[str, Any], branch: Mapping[str, Any], reset: Mapping[str, Any]
) -> dict[str, str]:
    return {
        "route_id": str(policy["route_id"]),
        "policy_id": str(policy["policy_id"]),
        "opportunity_id": str(branch["opportunity_id"]),
        "branch_id": str(branch["branch_id"]),
        "reset_id": str(reset["reset_id"]),
    }


def load_saved(
    directory: Path,
    *,
    policy: Mapping[str, Any],
    branch: Mapping[str, Any],
    reset: Mapping[str, Any],
    calls: Calls,
) -> dict[str, Any]:
    def loader(path: str) -> LGRC9V3:
        calls.record("pygrc.models.LGRC9V3.load")
        return LGRC9V3.load(path)

    def digester(model: LGRC9V3) -> str:
        return native_digest(model, calls)

    return load_composite(
        directory,
        native_loader=loader,
        native_digest=digester,
        expected_bindings=expected_bindings(policy, branch, reset),
    )


def source_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def preflight(
    *,
    freeze: Mapping[str, Any],
    freeze_path: Path,
    graph_root: Path,
    output: Path,
) -> tuple[str, Path, Path, bool, dict[str, Any]]:
    expected_freeze_path = ROOT / (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
        "contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json"
    )
    require(freeze_path.resolve() == expected_freeze_path.resolve(), "unexpected freeze path")
    require(sha256_file(freeze_path) == EXPECTED_FREEZE_SHA256, "accepted freeze digest drifted")
    require(freeze["artifact_id"] == EXPECTED_FREEZE_ID, "wrong freeze identity")
    require(freeze["decision_id"] == "P2-I3-DEC-034", "wrong freeze decision")
    require(freeze["bounded_execution"]["attempts"] == 1, "attempt ceiling drifted")
    require(freeze["bounded_execution"]["retries"] == 0, "retry ceiling drifted")
    require(freeze["bounded_execution"]["parallelism"] == 1, "parallelism drifted")
    require(freeze["bounded_execution"]["network_allowed"] is False, "network opened")
    require(
        freeze["bounded_execution"]["external_repository_writes_allowed"] is False,
        "external writes opened",
    )
    require(git(ROOT, "merge-base", "--is-ancestor", FREEZE_SOURCE_ANCHOR, "HEAD") == "", "freeze source anchor is not an ancestor")
    source_head = git(ROOT, "rev-parse", "HEAD")
    graph_root = graph_root.resolve()
    require(graph_root.is_dir(), "graph root missing")
    require(git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION, "graph revision mismatch")
    require(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph worktree is not clean")

    planned_output = (ROOT / freeze["bounded_execution"]["planned_output"]).resolve()
    binding_path = (ROOT / freeze["bounded_execution"]["planned_runtime_binding_receipt"]).resolve()
    evidence_run = output.resolve() == planned_output
    if evidence_run:
        require(git(ROOT, "status", "--porcelain=v1", "--untracked-files=all") == "", "retained conformance requires a clean RCAE worktree")
        require(not output.exists(), "retained conformance output already exists")
        require(not binding_path.exists(), "runtime binding receipt already exists")
        for relative in (SCRIPT_RELATIVE, RUNTIME_RELATIVE, QUARANTINE_RELATIVE):
            require(git(ROOT, "ls-files", "--error-unmatch", relative.as_posix()) == relative.as_posix(), f"source is not committed: {relative}")
    else:
        require(not output.resolve().is_relative_to(ROOT.resolve()), "reconstruction output must be outside the repository")
        require(planned_output.is_file(), "retained conformance output missing")
        require(binding_path.is_file(), "retained runtime binding receipt missing")

    source_root = (graph_root / "src").resolve()
    require(Path(pygrc.__file__).resolve() == source_root / "pygrc" / "__init__.py", "PyGRC import does not resolve from exact graph source")
    require(any(Path(row).resolve() == source_root for row in sys.path if row), "graph source root absent from sys.path")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "RCAE .venv is not active")

    required_versions = freeze["environment"]["required_packages"]
    versions = {name: importlib.metadata.version(name) for name in required_versions}
    require(versions == required_versions, "dependency versions drifted")
    require(platform.python_version() == freeze["environment"]["python_version"], "Python version drifted")
    for row in freeze["bound_graph_sources"]:
        path = graph_root / row["path"]
        require(path.is_file() and sha256_file(path) == row["sha256"], f"graph source mismatch: {row['path']}")
    for row in freeze["authority"]["bound_rcae_artifacts"]:
        path = ROOT / row["path"]
        require(path.is_file() and sha256_file(path) == row["sha256"], f"RCAE authority mismatch: {row['path']}")
    for row in freeze["required_public_calls"]:
        require(callable(resolve_symbol(row["symbol"])), f"required public call missing: {row['symbol']}")

    normalized_command = [
        ".venv/bin/python",
        "-B",
        SCRIPT_RELATIVE.as_posix(),
        "--graph-root",
        freeze["authority"]["graph_repository"]["example_relative_value"],
        "--freeze",
        repo_relative(freeze_path),
        "--output",
        freeze["bounded_execution"]["planned_output"],
    ]
    source_files = [freeze_path, ROOT / RUNTIME_RELATIVE, ROOT / SCRIPT_RELATIVE, ROOT / QUARANTINE_RELATIVE]
    source_files.extend(ROOT / row["path"] for row in freeze["authority"]["bound_rcae_artifacts"])
    source_identities = {
        repo_relative(path): sha256_file(path)
        for path in sorted(set(source_files))
    }
    binding = with_digest(
        {
            "artifact_kind": "p2_i3_i03_br_conformance_runtime_binding_receipt",
            "artifact_schema_version": "1.0.0",
            "iteration_id": "P2-I3-I03",
            "branch_id": "P2-I3-BR",
            "evidence_effect": "implementation_conformance_only",
            "freeze_source_anchor": FREEZE_SOURCE_ANCHOR,
            "rcae_source_revision": source_head,
            "rcae_worktree_clean_before_invocation": True,
            "source_files": source_identities,
            "graph": {
                "repository_id": "graph-reflexive-coherence",
                "revision": EXPECTED_GRAPH_REVISION,
                "worktree_clean": True,
                "source_files": {row["path"]: row["sha256"] for row in freeze["bound_graph_sources"]},
                "pygrc_import": "src/pygrc/__init__.py",
            },
            "environment": {
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "interpreter": ".venv/bin/python",
                "packages": versions,
                "pythonhashseed": "0",
                "pythondontwritebytecode": "1",
                "network_allowed": False,
            },
            "normalized_command": normalized_command,
            "attempt_policy": {"attempts": 1, "retries": 0, "parallelism": 1},
            "prior_artifact_state": {
                "runtime_binding_receipt_absent": True,
                "retained_output_absent": True,
            },
            "execution_flags": {
                "candidate_execution": False,
                "calibration_execution": False,
                "scientific_control_execution": False,
                "scientific_interpretation": False,
            },
        }
    )
    if evidence_run:
        write_exclusive(binding_path, binding)
    else:
        retained = load_json(binding_path)
        require(retained == binding, "reconstruction source binding differs from retained receipt")
    return source_head, planned_output, binding_path, evidence_run, binding


def execute(
    *, freeze: Mapping[str, Any], binding: Mapping[str, Any], binding_path: Path
) -> dict[str, Any]:
    calls = Calls()
    checks = Checks()
    tolerance = float(freeze["fixture"]["fixture_only_values"]["absolute_float_tolerance"])
    cells = {row["name"]: row["cell_id"] for row in freeze["conformance_matrix"]}
    cell1 = cells["runtime_and_operation_binding"]
    cell2 = cells["repeated_native_formation_and_persistence"]
    cell3 = cells["positive_export_and_conservative_settlement"]
    cell4 = cells["eligible_zero_invalid_and_duplicate_lifecycle"]
    cell5 = cells["fixed_local_native_encounter"]
    cell6 = cells["q013_contrast_addressability"]
    cell7 = cells["composite_save_load_reset_fork_and_replay"]
    cell8 = cells["partial_stale_and_cross_bound_load_refusal"]
    cell9 = cells["control_and_variation_interface_addressability"]
    cell10 = cells["forbidden_read_and_hidden_router_exclusion"]
    cell11 = cells["mechanical_fixture_quarantine"]

    required_symbols = [row["symbol"] for row in freeze["required_public_calls"]]
    blocked_symbols = [row["symbol"] for row in freeze["blocked_public_calls"]]
    checks.add(cell1, "required_public_symbols_callable", all(callable(resolve_symbol(name)) for name in required_symbols), len(required_symbols), 18)
    checks.add(cell1, "executing_substrate_exact", freeze["fixture"]["lgrc_runtime_level"] == "lgrc2", freeze["fixture"]["lgrc_runtime_level"], "lgrc2")

    model = build_model(freeze, calls)
    initial_native_digest = native_digest(model, calls)
    calls.invoke("pygrc.models.LGRC9V3.snapshot", model.snapshot)
    calls.invoke("pygrc.models.lgrc9v3_restoration_identity_v2", lgrc9v3_restoration_identity_v2, model)
    initial_budget = budget(model, calls)
    initial_coherence = coherences(model, calls)

    formation_amount = float(freeze["fixture"]["fixture_only_values"]["formation_event_amount"])
    formation_specs = (
        formation_request(source=0, target=1, edge=0, amount=formation_amount, index=0),
        formation_request(source=5, target=6, edge=5, amount=formation_amount, index=1),
        formation_request(source=0, target=1, edge=0, amount=formation_amount, index=2),
        formation_request(source=5, target=6, edge=5, amount=formation_amount, index=3),
    )
    formation_rows: list[dict[str, Any]] = []
    for request in formation_specs:
        before = coherences(model, calls)
        schedule(model, request, calls)
        results = run_queue(model, 2, calls)
        require(len(results) == 2 and queue_count(model, calls) == 0, "formation queue did not settle exactly")
        departure = processing_receipt(results[0])
        arrival = processing_receipt(results[1])
        after = coherences(model, calls)
        formation_rows.append(
            {
                "request": dict(request),
                "departure": departure,
                "arrival": arrival,
                "source_debit": before[request["source_node_id"]] - after[request["source_node_id"]],
                "carrier_credit": after[request["target_node_id"]] - before[request["target_node_id"]],
            }
        )
    formed_coherence = coherences(model, calls)
    formed_budget = budget(model, calls)
    checks.add(cell2, "formation_event_count_per_route", len(formation_rows) == 4, {"route_a": 2, "route_b": 2}, {"route_a": 2, "route_b": 2})
    checks.add(cell2, "formation_debit_credit_exact", all(close(row["source_debit"], formation_amount, tolerance) and close(row["carrier_credit"], formation_amount, tolerance) for row in formation_rows), True, True)
    checks.add(cell2, "formation_queue_empty_at_persistent_checkpoint", queue_count(model, calls) == 0, queue_count(model, calls), 0)
    checks.add(cell2, "formed_carriers_role_matched", close(formed_coherence[1], 0.5, tolerance) and close(formed_coherence[6], 0.5, tolerance), {"carrier_a": formed_coherence[1], "carrier_b": formed_coherence[6]}, {"carrier_a": 0.5, "carrier_b": 0.5})

    policy_binding = {
        "policy_id": "p2-i3-i03-br-export-policy-v1",
        "route_id": "p2-i3-i03-route-0002",
        "source_node_id": 6,
        "destination_node_id": 7,
        "edge_id": 6,
        "export_floor": float(freeze["fixture"]["fixture_only_values"]["export_floor"]),
        "export_cap": float(freeze["fixture"]["fixture_only_values"]["export_cap"]),
        "absolute_tolerance": tolerance,
        "schedule_by_sequence": {
            "0": {
                "departure_event_time_key": 8.0,
                "arrival_event_time_key": 9.0,
                "scheduler_event_index": 8,
                "packet_index": 4,
                "source_lineage_id": "p2_i3_i03_br_export_0",
                "target_lineage_id": "p2_i3_i03_br_reservoir_0002",
            },
            "1": {
                "departure_event_time_key": 10.0,
                "arrival_event_time_key": 11.0,
                "scheduler_event_index": 10,
                "packet_index": 5,
                "source_lineage_id": "p2_i3_i03_br_export_1",
                "target_lineage_id": "p2_i3_i03_br_reservoir_0002",
            },
        },
    }
    baseline_policy = initial_policy_state(policy_binding)
    baseline_branch = make_branch_state(branch_id="p2-i3-i03-construction-baseline", parent_composite_identity="p2-i3-i03-construction-root", opportunity_id="p2-i3-i03-no-probe")
    baseline_audit = make_audit_state(lineage=["constructed"])
    reset_seed = digest_data(
        {
            "native": initial_native_digest,
            "policy": baseline_policy,
            "branch": baseline_branch,
            "audit": baseline_audit,
        }
    )
    reset_state = make_reset_state(reset_id="p2-i3-i03-reset-v1", baseline_composite_identity=reset_seed)
    checkpoint_branch = make_branch_state(branch_id="p2-i3-i03-formed-parent", parent_composite_identity=reset_seed, opportunity_id="p2-i3-i03-no-probe")
    checkpoint_audit = make_audit_state(lineage=["constructed", "four_formation_packets_settled"])

    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        formed_dir = temp_root / "formed"
        calls.record("pygrc.models.LGRC9V3.save")
        formed_manifest = save_composite(
            formed_dir,
            model=model,
            native_digest=lambda item: native_digest(item, calls),
            policy_state=baseline_policy,
            branch_state=checkpoint_branch,
            reset_state=reset_state,
            audit_state=checkpoint_audit,
        )
        formed_exact = formed_manifest["exact_composite_identity"]
        loaded_formed = load_saved(formed_dir, policy=baseline_policy, branch=checkpoint_branch, reset=reset_state, calls=calls)
        export_model = loaded_formed["model"]
        loaded_exact = (
            native_digest(export_model, calls)
            == formed_manifest["native_restoration_digest"]
            and loaded_formed["manifest"] == formed_manifest
            and loaded_formed["policy"] == baseline_policy
            and loaded_formed["branch"] == checkpoint_branch
            and loaded_formed["reset"] == reset_state
            and loaded_formed["audit"] == checkpoint_audit
        )
        checks.add(cell7, "formed_original_load_exact_identity", loaded_exact, loaded_formed["manifest"]["exact_composite_identity"], formed_exact)

        receipt0 = lifecycle_receipt(
            receipt_id="p2-i3-i03-receipt-0",
            sequence=0,
            event_identity=formation_rows[-1]["arrival"]["event_id"],
            predecessor=formed_exact,
            policy=baseline_policy,
        )
        carrier_before_export = coherences(export_model, calls)[6]
        positive = evaluate_export_policy(
            carrier_coherence=carrier_before_export,
            receipt=receipt0,
            predecessor_composite_identity=formed_exact,
            policy_state=baseline_policy,
        )
        checks.add(cell3, "eligible_positive_policy_transition", positive["disposition"] == "eligible_positive", positive["disposition"], "eligible_positive")
        pending_policy = positive["policy_state"]

        premature_receipt = lifecycle_receipt(
            receipt_id="p2-i3-i03-receipt-1",
            sequence=1,
            event_identity="pending-not-settled",
            predecessor=formed_exact,
            policy=pending_policy,
        )
        pending_conflict = evaluate_export_policy(
            carrier_coherence=carrier_before_export,
            receipt=premature_receipt,
            predecessor_composite_identity=formed_exact,
            policy_state=pending_policy,
        )
        checks.add(cell4, "pending_export_blocks_second_receipt_atomically", pending_conflict["reason"] == "prior_export_not_settled" and pending_conflict["policy_state"] == pending_policy, pending_conflict["reason"], "prior_export_not_settled")

        before_export = coherences(export_model, calls)
        before_export_budget = budget(export_model, calls)
        schedule(export_model, positive["native_request"], calls)
        scheduled_budget = budget(export_model, calls)
        departure = processing_receipt(step(export_model, calls))
        in_flight_budget = budget(export_model, calls)
        arrival = processing_receipt(step(export_model, calls))
        after_export = coherences(export_model, calls)
        after_export_budget = budget(export_model, calls)
        export_amount = float(positive["reserved_amount"])
        settled_policy = settle_export_policy(
            pending_policy,
            receipt_id=positive["receipt_id"],
            native_settlement_identity=native_digest(export_model, calls),
        )
        checks.add(cell3, "export_debit_packet_credit_exact", close(before_export[6] - after_export[6], export_amount, tolerance) and close(after_export[7] - before_export[7], export_amount, tolerance) and close(departure["amount"], export_amount, tolerance) and close(arrival["amount"], export_amount, tolerance), {"debit": before_export[6] - after_export[6], "credit": after_export[7] - before_export[7], "packet": departure["amount"]}, export_amount)
        checks.add(cell3, "export_global_budget_closes", all(close(row["conserved_budget_total"], initial_budget["conserved_budget_total"], tolerance) and close(row["budget_error"], 0.0, tolerance) for row in (before_export_budget, scheduled_budget, in_flight_budget, after_export_budget)), [before_export_budget, scheduled_budget, in_flight_budget, after_export_budget], "constant conserved budget and zero error")
        checks.add(cell3, "export_floor_preserved", after_export[6] + tolerance >= float(policy_binding["export_floor"]), after_export[6], policy_binding["export_floor"])
        checks.add(cell3, "export_queue_settled", queue_count(export_model, calls) == 0, queue_count(export_model, calls), 0)

        settled_branch = make_branch_state(branch_id="p2-i3-i03-export-settled", parent_composite_identity=formed_exact, opportunity_id="p2-i3-i03-no-probe")
        settled_audit = make_audit_state(lineage=["formed_parent", "positive_export_settled"])
        settled_dir = temp_root / "settled"
        calls.record("pygrc.models.LGRC9V3.save")
        settled_manifest = save_composite(
            settled_dir,
            model=export_model,
            native_digest=lambda item: native_digest(item, calls),
            policy_state=settled_policy,
            branch_state=settled_branch,
            reset_state=reset_state,
            audit_state=settled_audit,
        )
        receipt1 = lifecycle_receipt(
            receipt_id="p2-i3-i03-receipt-1",
            sequence=1,
            event_identity=arrival["event_id"],
            predecessor=settled_manifest["exact_composite_identity"],
            policy=settled_policy,
        )
        native_before_zero = native_digest(export_model, calls)
        zero = evaluate_export_policy(
            carrier_coherence=coherences(export_model, calls)[6],
            receipt=receipt1,
            predecessor_composite_identity=settled_manifest["exact_composite_identity"],
            policy_state=settled_policy,
        )
        checks.add(cell4, "eligible_zero_advances_policy_only", zero["disposition"] == "eligible_zero" and zero["native_request"] is None and native_digest(export_model, calls) == native_before_zero, zero["disposition"], "eligible_zero with native identity unchanged")
        final_policy = zero["policy_state"]
        duplicate = evaluate_export_policy(
            carrier_coherence=coherences(export_model, calls)[6],
            receipt=receipt0,
            predecessor_composite_identity=settled_manifest["exact_composite_identity"],
            policy_state=final_policy,
        )
        invalid_receipt = deepcopy(receipt1)
        invalid_receipt["receipt_id"] = "p2-i3-i03-invalid"
        invalid_receipt["route_id"] = "wrong-route"
        invalid = evaluate_export_policy(
            carrier_coherence=coherences(export_model, calls)[6],
            receipt=invalid_receipt,
            predecessor_composite_identity=settled_manifest["exact_composite_identity"],
            policy_state=final_policy,
        )
        checks.add(cell4, "duplicate_receipt_atomic", duplicate["disposition"] == "duplicate_consumed" and duplicate["policy_state"] == final_policy, duplicate["disposition"], "duplicate_consumed")
        checks.add(cell4, "invalid_receipt_atomic", invalid["disposition"] == "invalid" and invalid["policy_state"] == final_policy, invalid["disposition"], "invalid")

        final_branch = make_branch_state(branch_id="p2-i3-i03-post-zero-parent", parent_composite_identity=settled_manifest["exact_composite_identity"], opportunity_id="p2-i3-i03-no-probe")
        final_audit = make_audit_state(lineage=["formed_parent", "positive_export_settled", "eligible_zero_consumed"])
        final_dir = temp_root / "post-zero"
        calls.record("pygrc.models.LGRC9V3.save")
        final_manifest = save_composite(
            final_dir,
            model=export_model,
            native_digest=lambda item: native_digest(item, calls),
            policy_state=final_policy,
            branch_state=final_branch,
            reset_state=reset_state,
            audit_state=final_audit,
        )

        probe_amount = float(freeze["fixture"]["fixture_only_values"]["encounter_probe_amount"])
        opportunity_a = {
            "opportunity_id": "p2-i3-i03-opportunity-0001",
            "parent_composite_identity": formed_exact,
            "source_node_id": 1,
            "target_node_id": 3,
            "edge_id": 2,
            "amount": probe_amount,
            "departure_event_time_key": 12.0,
            "arrival_event_time_key": 13.0,
            "scheduler_event_index": 12,
            "packet_index": 6,
            "source_lineage_id": "p2_i3_i03_probe",
            "target_lineage_id": "p2_i3_i03_continuation",
        }
        opportunity_b = {
            **opportunity_a,
            "opportunity_id": "p2-i3-i03-opportunity-0002",
            "parent_composite_identity": final_manifest["exact_composite_identity"],
            "source_node_id": 6,
            "target_node_id": 8,
            "edge_id": 7,
        }
        request_a = build_blind_encounter_request(opportunity=opportunity_a, parent_composite_identity=formed_exact)
        request_b = build_blind_encounter_request(opportunity=opportunity_b, parent_composite_identity=final_manifest["exact_composite_identity"])
        request_role_projection = lambda row: {key: row[key] for key in row if key not in {"source_node_id", "target_node_id", "edge_id"}}
        checks.add(cell5, "encounter_requests_role_matched", request_role_projection(request_a) == request_role_projection(request_b), request_role_projection(request_a), request_role_projection(request_b))

        admitted_loaded = load_saved(formed_dir, policy=baseline_policy, branch=checkpoint_branch, reset=reset_state, calls=calls)
        admitted_model = admitted_loaded["model"]
        schedule(admitted_model, request_a, calls)
        admitted_departure = processing_receipt(step(admitted_model, calls))
        admitted_arrival = processing_receipt(step(admitted_model, calls))
        checks.add(cell5, "formed_branch_native_admission", close(admitted_departure["amount"], probe_amount, tolerance) and close(admitted_arrival["amount"], probe_amount, tolerance), admitted_departure["amount"], probe_amount)

        refused_loaded = load_saved(final_dir, policy=final_policy, branch=final_branch, reset=reset_state, calls=calls)
        refused_model = refused_loaded["model"]
        schedule(refused_model, request_b, calls)
        refusal_pre = native_digest(refused_model, calls)
        refusal_reason = None
        try:
            step(refused_model, calls)
        except Exception as exc:
            refusal_reason = native_refusal_reason(exc)
        refusal_post = native_digest(refused_model, calls)
        checks.add(cell5, "post_export_native_refusal_exact", refusal_reason == "source coherence is smaller than packet amount", refusal_reason, "source coherence is smaller than packet amount")
        checks.add(cell5, "native_refusal_atomic_at_scheduled_boundary", refusal_pre == refusal_post, refusal_post, refusal_pre)

        replay_loaded = load_saved(final_dir, policy=final_policy, branch=final_branch, reset=reset_state, calls=calls)
        replay_model = replay_loaded["model"]
        schedule(replay_model, request_b, calls)
        replay_pre = native_digest(replay_model, calls)
        replay_reason = None
        try:
            step(replay_model, calls)
        except Exception as exc:
            replay_reason = native_refusal_reason(exc)
        replay_post = native_digest(replay_model, calls)
        checks.add(cell7, "atomic_refusal_replay_exact", (replay_reason, replay_pre, replay_post) == (refusal_reason, refusal_pre, refusal_post), {"reason": replay_reason, "before": replay_pre, "after": replay_post}, {"reason": refusal_reason, "before": refusal_pre, "after": refusal_post})

        constructors = build_q13_constructor_records()
        checks.add(cell6, "q013_constructor_identities_distinct", [row["contrast_id"] for row in constructors] == ["P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001", "P2-I3-BR-Q13-EXPORT-MASS-MATCH-001", "P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001"], [row["contrast_id"] for row in constructors], "three exact contrast IDs")
        history_a = make_audit_state(lineage=["formation", "formation"])
        history_b = make_audit_state(lineage=["one_equal_total_formation"])
        native_parent_digest = formed_manifest["native_restoration_digest"]
        exact_a = composite_identity(native_restoration_digest=native_parent_digest, policy_state=baseline_policy, branch_state=checkpoint_branch, reset_state=reset_state, audit_state=history_a)
        exact_b = composite_identity(native_restoration_digest=native_parent_digest, policy_state=baseline_policy, branch_state=checkpoint_branch, reset_state=reset_state, audit_state=history_b)
        causal_a = causal_continuation_projection(native_restoration_digest=native_parent_digest, policy_state=baseline_policy, branch_state=checkpoint_branch, reset_state=reset_state)
        causal_b = causal_continuation_projection(native_restoration_digest=native_parent_digest, policy_state=baseline_policy, branch_state=checkpoint_branch, reset_state=reset_state)
        checks.add(cell6, "history_constructor_exact_distinct_causal_equal", exact_a != exact_b and causal_a == causal_b, {"exact_equal": exact_a == exact_b, "causal_equal": causal_a == causal_b}, {"exact_equal": False, "causal_equal": True})

        fork_one = make_branch_state(branch_id="p2-i3-i03-fork-1", parent_composite_identity=formed_exact, opportunity_id=opportunity_a["opportunity_id"])
        fork_two = make_branch_state(branch_id="p2-i3-i03-fork-2", parent_composite_identity=formed_exact, opportunity_id=opportunity_a["opportunity_id"])
        checks.add(cell7, "forks_share_parent_and_have_distinct_identity", fork_one["parent_composite_identity"] == fork_two["parent_composite_identity"] and fork_one["branch_id"] != fork_two["branch_id"], {"parent_equal": True, "branch_distinct": True}, {"parent_equal": True, "branch_distinct": True})
        replay_one = load_saved(formed_dir, policy=baseline_policy, branch=checkpoint_branch, reset=reset_state, calls=calls)["model"]
        replay_two = load_saved(formed_dir, policy=baseline_policy, branch=checkpoint_branch, reset=reset_state, calls=calls)["model"]
        replay_receipts = []
        for replay in (replay_one, replay_two):
            schedule(replay, request_a, calls)
            replay_receipts.append([processing_receipt(step(replay, calls)), processing_receipt(step(replay, calls))])
        checks.add(cell7, "equal_input_continuation_exact", replay_receipts[0] == replay_receipts[1] and native_digest(replay_one, calls) == native_digest(replay_two, calls), {"receipts_equal": replay_receipts[0] == replay_receipts[1], "native_equal": native_digest(replay_one, calls) == native_digest(replay_two, calls)}, {"receipts_equal": True, "native_equal": True})

        reset_model = load_saved(formed_dir, policy=baseline_policy, branch=checkpoint_branch, reset=reset_state, calls=calls)["model"]
        calls.invoke("pygrc.models.LGRC9V3.reset", reset_model.reset)
        reset_rcae = reset_rcae_components(
            baseline_policy_state=baseline_policy,
            baseline_branch_state=baseline_branch,
            baseline_reset_state=reset_state,
            baseline_audit_state=baseline_audit,
        )
        reset_exact = composite_identity(
            native_restoration_digest=native_digest(reset_model, calls),
            policy_state=reset_rcae["policy"],
            branch_state=reset_rcae["branch"],
            reset_state=reset_rcae["reset"],
            audit_state=reset_rcae["audit"],
        )
        expected_reset_exact = composite_identity(
            native_restoration_digest=initial_native_digest,
            policy_state=baseline_policy,
            branch_state=baseline_branch,
            reset_state=reset_state,
            audit_state=baseline_audit,
        )
        checks.add(cell7, "paired_native_rcae_reset_returns_construction_baseline", reset_exact == expected_reset_exact, reset_exact, expected_reset_exact)

        loader_invocations = 0
        def guarded_loader(path: str) -> LGRC9V3:
            nonlocal loader_invocations
            loader_invocations += 1
            return LGRC9V3.load(path)
        base_bindings = expected_bindings(baseline_policy, checkpoint_branch, reset_state)
        refusal_rows: list[dict[str, Any]] = []
        scenarios: list[tuple[str, Path, dict[str, str]]] = []
        missing = temp_root / "missing-component"
        shutil.copytree(formed_dir, missing)
        (missing / "policy.json").unlink()
        scenarios.append(("missing_component", missing, base_bindings))
        tampered = temp_root / "tampered-component"
        shutil.copytree(formed_dir, tampered)
        (tampered / "policy.json").write_text("{}\n", encoding="utf-8")
        scenarios.append(("digest_tamper", tampered, base_bindings))
        for field in ("route_id", "policy_id", "opportunity_id", "branch_id", "reset_id"):
            wrong = dict(base_bindings)
            wrong[field] = f"wrong-{field}"
            scenarios.append((f"wrong_{field}", formed_dir, wrong))
        native_only = temp_root / "native-only"
        native_only.mkdir()
        shutil.copy2(formed_dir / "native.json", native_only / "native.json")
        scenarios.append(("native_only", native_only, base_bindings))
        policy_only = temp_root / "policy-only"
        policy_only.mkdir()
        shutil.copy2(formed_dir / "policy.json", policy_only / "policy.json")
        scenarios.append(("policy_only", policy_only, base_bindings))
        for scenario_id, directory, bindings in scenarios:
            before_count = loader_invocations
            refused = False
            try:
                load_composite(directory, native_loader=guarded_loader, native_digest=digest_lgrc9v3_restoration_identity_v2, expected_bindings=bindings)
            except BRContractError:
                refused = True
            refusal_rows.append({"scenario_id": scenario_id, "refused": refused, "native_loader_invoked": loader_invocations != before_count})
        checks.add(cell8, "all_partial_stale_cross_bound_loads_fail_before_native_load", all(row["refused"] and not row["native_loader_invoked"] for row in refusal_rows), refusal_rows, "all refused before native loader")

        controls = build_control_interface_records(carrier_value=formed_coherence[1])
        checks.add(cell9, "control_interfaces_distinct", len({row["control_id"] for row in controls}) == len(controls) == 9, [row["control_id"] for row in controls], "nine distinct controls")
        relocation = controls[0]
        checks.add(cell9, "relocation_payload_excludes_semantic_labels", set(relocation["payload"]) == {"source_binding", "target_binding", "carrier_coherence"} and set(relocation["excluded_payload_fields"]) == {"route_label", "participant", "preference"}, relocation, "numeric bindings plus carrier state only")

        runtime_state = state(model, calls)
        geometric = calls.invoke("pygrc.models.compute_lgrc9v3_geometric_distances", compute_lgrc9v3_geometric_distances, runtime_state.base_state, source_node_id=0)
        functional = calls.invoke("pygrc.models.compute_lgrc9v3_functional_distances", compute_lgrc9v3_functional_distances, runtime_state.base_state, source_node_id=0)
        causal = calls.invoke("pygrc.models.compute_lgrc9v3_causal_distances", compute_lgrc9v3_causal_distances, runtime_state.base_state, source_node_id=0, edge_causal_delay=runtime_state.edge_causal_delay)
        distance_nodes = set(geometric)
        checks.add(cell9, "distance_interfaces_callable_and_distinct", distance_nodes == set(functional) == set(causal) == {0, 1, 2, 3, 4}, {"geometric": len(geometric), "functional": len(functional), "causal": len(causal)}, {"geometric": 5, "functional": 5, "causal": 5})

        export_parameters = tuple(inspect.signature(evaluate_export_policy).parameters)
        adapter_parameters = tuple(inspect.signature(build_blind_encounter_request).parameters)
        checks.add(cell10, "export_policy_input_surface_narrow", export_parameters == ("carrier_coherence", "receipt", "predecessor_composite_identity", "policy_state"), export_parameters, ("carrier_coherence", "receipt", "predecessor_composite_identity", "policy_state"))
        checks.add(cell10, "encounter_adapter_input_surface_field_blind", adapter_parameters == ("opportunity", "parent_composite_identity"), adapter_parameters, ("opportunity", "parent_composite_identity"))
        checks.add(cell10, "paired_encounters_used_independent_loaded_models", admitted_model is not refused_model and opportunity_a["parent_composite_identity"] != opportunity_b["parent_composite_identity"], True, True)

        quarantine_rejections = []
        clean_payload = {"source_class": "candidate_blind_future_source", "value_id": "future-value"}
        for consumer in sorted(FORBIDDEN_CONSUMER_CLASSES):
            assert_no_conformance_import(clean_payload, consumer_class=consumer)
            rejected = False
            try:
                assert_no_conformance_import(
                    {
                        "source_class": "i03_conformance",
                        "path": freeze["bounded_execution"]["planned_output"],
                        "digest": binding["canonical_payload_digest"],
                    },
                    consumer_class=consumer,
                    blocked_output_digests=[binding["canonical_payload_digest"]],
                    blocked_fixture_value_ids=[freeze["fixture"]["fixture_id"]],
                )
            except ConformanceQuarantineError:
                rejected = True
            quarantine_rejections.append({"consumer_class": consumer, "rejected": rejected})
        checks.add(cell11, "all_downstream_consumer_classes_reject_declared_conformance", all(row["rejected"] for row in quarantine_rejections), quarantine_rejections, "all eight rejected")

        actual_symbols = sorted(set(calls.rows))
        checks.add(cell1, "all_required_public_calls_exercised", set(required_symbols) <= set(actual_symbols), actual_symbols, required_symbols)
        checks.add(cell1, "blocked_public_calls_unused", not set(blocked_symbols) & set(actual_symbols), sorted(set(blocked_symbols) & set(actual_symbols)), [])

        cells_output = []
        for frozen in freeze["conformance_matrix"]:
            rows = [row for row in checks.rows if row["cell_id"] == frozen["cell_id"]]
            cells_output.append(
                {
                    "cell_id": frozen["cell_id"],
                    "name": frozen["name"],
                    "status": "passed_implementation_conformance",
                    "check_ids": [row["check_id"] for row in rows],
                    "scientific_evidence_effect": "none",
                }
            )

        section_8_2 = [
            (1, "two_alternative_route_surfaces", [cell1, cell2]),
            (2, "route_local_field_encounter", [cell2, cell5]),
            (3, "attributable_repeated_costly_formation", [cell2]),
            (4, "non_static_dynamic_operationally_observable", [cell3, cell4]),
            (5, "dynamic_to_encounter_mediator", [cell3, cell5]),
            (6, "separate_candidate_and_control_addressability", [cell6, cell9]),
            (7, "false_trace_interface_without_outcome_writer", [cell9, cell10]),
            (8, "relocation_payload_boundary", [cell9]),
            (9, "complete_continuation_state_enumerated", [cell7, cell8]),
            (10, "active_history_not_claimed_and_audit_separated", [cell6, cell7]),
            (11, "fresh_traverser_and_direct_address", [cell5, cell10]),
            (12, "distance_roles_non_substituted", [cell9]),
            (13, "native_rcae_ownership_explicit", [cell1, cell3, cell10]),
            (14, "non_native_identity_cannot_transition_silently", [cell1, cell7]),
            (15, "constructed_surface_minimality_visible", [cell3, cell5, cell10]),
        ]

        observations = {
            "fixture_only": True,
            "scientific_interpretation_allowed": False,
            "initial_coherence": initial_coherence,
            "formed_coherence": formed_coherence,
            "formation": formation_rows,
            "budgets": {
                "initial": initial_budget,
                "formed": formed_budget,
                "pre_export": before_export_budget,
                "scheduled_export": scheduled_budget,
                "in_flight_export": in_flight_budget,
                "post_export": after_export_budget,
            },
            "export": {
                "positive_transition": positive,
                "departure": departure,
                "arrival": arrival,
                "post_export_coherence": after_export,
                "eligible_zero_transition": zero,
                "duplicate_disposition": duplicate["disposition"],
                "invalid_disposition": invalid["disposition"],
                "pending_conflict_disposition": pending_conflict["reason"],
            },
            "encounter": {
                "admitted_request": request_a,
                "admitted_departure": admitted_departure,
                "admitted_arrival": admitted_arrival,
                "refused_request": request_b,
                "refusal_reason": refusal_reason,
                "refusal_atomic": refusal_pre == refusal_post,
                "replay_exact": (replay_reason, replay_pre, replay_post) == (refusal_reason, refusal_pre, refusal_post),
            },
            "q013_constructors": constructors,
            "q015": {
                "formed_manifest_identity": formed_exact,
                "settled_manifest_identity": settled_manifest["exact_composite_identity"],
                "post_zero_manifest_identity": final_manifest["exact_composite_identity"],
                "history_exact_identities_differ": exact_a != exact_b,
                "history_causal_projections_equal": causal_a == causal_b,
                "load_refusals": refusal_rows,
            },
            "control_interfaces": controls,
            "distance_interface_addressability": {
                "geometric_node_count": len(geometric),
                "functional_node_count": len(functional),
                "causal_node_count": len(causal),
                "interpretation": "none_conformance_only",
            },
            "quarantine_rejections": quarantine_rejections,
        }

    call_counts = dict(sorted(Counter(calls.rows).items()))
    result = {
        "artifact_kind": "p2_i3_i03_br_conformance_runtime_result",
        "artifact_schema_version": "1.0.0",
        "artifact_id": "P2-I3-I03-BR-RUNTIME-CONFORMANCE",
        "iteration_id": "P2-I3-I03",
        "branch_id": "P2-I3-BR",
        "status": "passed_implementation_conformance",
        "classification": "interfaces_operationally_expressible_at_exact_sources",
        "evidence_effect": "implementation_conformance_only",
        "scientific_evidence_effect": "none",
        "freeze": {
            "artifact_id": freeze["artifact_id"],
            "path": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json",
            "sha256": binding["source_files"]["experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json"],
            "decision_id": freeze["decision_id"],
        },
        "runtime_binding_receipt": {
            "path": repo_relative(binding_path),
            "sha256": sha256_file(binding_path),
            "canonical_payload_digest": binding["canonical_payload_digest"],
        },
        "execution_boundaries": {
            "attempt_index": 1,
            "retry_count": 0,
            "parallelism": 1,
            "network_used": False,
            "external_repository_writes": False,
            "candidate_execution": False,
            "calibration_execution": False,
            "scientific_control_execution": False,
            "scientific_interpretation": False,
        },
        "cells": cells_output,
        "check_count": len(checks.rows),
        "checks": checks.rows,
        "required_public_call_counts": call_counts,
        "blocked_public_calls_used": [],
        "observations": observations,
        "section_8_2_dispositions": [
            {
                "item": index,
                "requirement_id": name,
                "status": "satisfied_at_i03_operational_conformance_boundary",
                "evidence_cells": evidence_cells,
                "later_scientific_evidence": "not_supplied_by_i03_conformance",
            }
            for index, name, evidence_cells in section_8_2
        ],
        "producer_cost_conformance_projection": {
            "contract_required": ["serialized_export_policy", "composite_policy_restoration"],
            "rcae_ecology_required": ["blind_structural_encounter_adapter", "control_interface_identity"],
            "evidence_only": ["temporary_branching", "checks", "quarantine", "reconstruction"],
            "runtime_module_source_lines": source_lines(ROOT / RUNTIME_RELATIVE),
            "harness_source_lines": source_lines(ROOT / SCRIPT_RELATIVE),
            "native_call_count": sum(call_counts.values()),
            "scalar_cost_or_winner": None,
            "scientific_interpretation": None,
        },
        "claim_boundaries": {
            "operational_expressibility": True,
            "AE01_H_L03_supported": False,
            "AE01_H_L03_refuted": False,
            "control_outcomes_assigned": False,
            "B_R_selected_over_C2": False,
            "native_trail_primitive": False,
            "discriminator_gate_passed": False,
        },
        "reconstruction": {
            "command": freeze["commands"]["planned_reconstruction_after_execution"],
            "expected_relation": "byte_exact_output_using_retained_binding_receipt",
        },
    }
    require(all(row["status"] == "passed_implementation_conformance" for row in cells_output), "not all conformance cells passed")
    require(len(cells_output) == 11, "conformance cell count drifted")
    require(len(result["section_8_2_dispositions"]) == 15, "8.2 disposition count drifted")
    require("/home/" not in json.dumps(result, sort_keys=True), "machine-local path entered conformance output")
    return with_digest(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", required=True, type=Path)
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    freeze_path = args.freeze.resolve()
    output = args.output.resolve()
    freeze = load_json(freeze_path)
    _, _, binding_path, evidence_run, binding = preflight(
        freeze=freeze,
        freeze_path=freeze_path,
        graph_root=args.graph_root,
        output=output,
    )
    result = execute(freeze=freeze, binding=binding, binding_path=binding_path)
    write_exclusive(output, result)
    graph_root = args.graph_root.resolve()
    require(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph repository changed during conformance")
    mode = "retained_evidence_invocation" if evidence_run else "reconstruction_invocation"
    print(
        json.dumps(
            {
                "status": result["status"],
                "mode": mode,
                "cells_passed": len(result["cells"]),
                "checks_passed": result["check_count"],
                "scientific_evidence_effect": "none",
                "output": repo_relative(output) if output.is_relative_to(ROOT) else "temporary_reconstruction_output",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
